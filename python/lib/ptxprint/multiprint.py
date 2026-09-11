import os, argparse
import logging
import time
from configparser import ConfigParser
from dataclasses import dataclass
from typing import Union, Any, Optional
from concurrent.futures import ProcessPoolExecutor, Future, as_completed
from concurrent.futures import wait as wait_futures
import multiprocessing as mp
import threading, queue, psutil
from ptxprint.page_filler import PTXFiller
from ptxprint.project import ProjectList
from ptxprint.utils import BuildParams, ProgressEvent, f_
from usfmtc.reference import chaps, RefList


class ViewPrinter:
    """Printer wrapper for view-based rendering jobs, mirroring PTXFiller's interface."""
    def __init__(self, build_params, nid: str, progress_q=None):
        self.build_params = build_params
        self.nid = nid
        self.progress_q = progress_q
        self.timedout = False
        self.cancelled = False

        self.view = ViewModel(
            build_params.prjtree,
            build_params.config,
            build_params.scriptsdir,
            build_params.args
        )
        self.view.setup_ini()
        self.view.setPrjid(build_params.pid, build_params.guid, loadConfig=False, startup=True)

    def solve(self, books: list[str], cfgid_override: Optional[str] = None):
        cfgid = cfgid_override or self.build_params.cfgid
        self.view.setConfigId(cfgid)
        self.view.set("ecb_booklist", books)
        self.view.set("r_book", "multiple")

        runjob = RunJob(
            self.view,
            self.build_params.scriptsdir,
            self.build_params.macrosdir,
            self.build_params.args
        )
        runjob.nothreads = True
        runjob.silent = True
        res = runjob.doit(noview=True, noaction=False)
        if self.build_params.resultfn is not None:
            res = self.build_params.resultfn(self.view)
        return res


@dataclass
class Job:
    action: str                       # 'fill' or 'print'
    books: list[str]                  # List of book IDs
    build_params: BuildParams         # BuildParams object
    log_config: Optional[dict] = None
    stop: bool = False
    cfgid: Optional[str] = None


class GLibCompatQueue:
    """A progress queue safe to share with worker processes on Windows.

    Workers (child processes) call put() which writes to the inner mp.Queue.
    mp.Queue is picklable, so Worker instances can be spawned on Windows.

    The main process polls for events using get_nowait(), called periodically
    by a GLib.timeout_add callback — no socket pair or relay thread needed.

    The GLibCompatQueue itself is NOT pickled into workers — only the inner
    mp.Queue is passed (see __getstate__ / __setstate__).
    """

    def __init__(self, ctx=None):
        if ctx is None:
            ctx = mp
        self._mp_queue = ctx.Queue()

    def put(self, item):
        """Called by worker processes (or main process for single-book jobs)."""
        self._mp_queue.put(item)

    def get_nowait(self):
        """Return the next item without blocking, or raise queue.Empty."""
        return self._mp_queue.get_nowait()

    def close(self):
        try:
            self._mp_queue.close()
            self._mp_queue.join_thread()
        except Exception:
            pass

    def join_thread(self):
        pass

    def clear(self):
        try:
            while True:
                self._mp_queue.get_nowait()
        except (queue.Empty, ValueError):
            pass

    # --- Pickling support ---
    # When Worker (mp.Process) is pickled for spawning on Windows, only the
    # inner mp.Queue crosses the process boundary.
    def __getstate__(self):
        return {'_mp_queue': self._mp_queue}

    def __setstate__(self, state):
        # In the child process: only restore put() capability via _mp_queue.
        self._mp_queue = state['_mp_queue']


class WorkerContext:
    """Manages worker lifecycle, cached printer instance, and job watchdog execution."""
    def __init__(self, nid: str, progress_q, cancel_event):
        self.nid = nid
        self.progress_q = progress_q
        self.cancel_event = cancel_event

        self.last_job: Optional[Job] = None
        self.current_printer: Optional[Union[PTXFiller, ViewPrinter]] = None

    def matches_last_job(self, new_job: Job) -> bool:
        """Determines if the cached printer instance can be reused for the incoming job."""
        if self.last_job is None or self.current_printer is None:
            return False
        return (
            self.last_job.action == new_job.action and
            self.last_job.build_params == new_job.build_params and
            self.last_job.cfgid == new_job.cfgid
        )

    def get_printer(self, job: Job):
        """Returns the active printer, creating a new instance if job configuration changed."""
        if not self.matches_last_job(job):
            if job.action == 'fill':
                self.current_printer = PTXFiller(job.build_params, self.nid, progress_q=self.progress_q)
                logging.debug(f"{self.current_printer=}")
            elif job.action == 'print':
                self.current_printer = ViewPrinter(job.build_params, self.nid, progress_q=self.progress_q)
            else:
                raise ValueError(f"Unknown job action: {job.action}")
            self.last_job = job
        else:
            logging.debug("new job matches old job, using that")
        # always set up the view even if same as before
        if job.action == 'print' and job.build_params.setupfn is not None:
            job.build_params.setupfn(self.current_printer.view, job.build_params.setup_args)

        return self.current_printer

    def setup_logger(self, build_params, log_config, target_id: str):
        if not log_config or build_params.loglevel is None:
            return
        ext = f"pbuild{self.nid}" if self.nid is not None else None
        project = build_params.prjtree.findProject(build_params.pid)
        log_dir = project.printPath(build_params.cfgid, ext=ext)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"ptxprint_{target_id}.log")

        logging.basicConfig(
            filename=log_file, filemode="w", encoding="utf-8",
            force=True, **log_config
        )
        logging.info(f"Opened log file {time.asctime()}")

    def execute_job(self, job: Job):
        """Unified execution handler with shared watchdog timer and logger setup."""
        target_id = job.books[0] if job.action == 'fill' else "_".join(job.books)

        logging.debug(f"Executing for {target_id}")
        if self.cancel_event and self.cancel_event.value:
            return (target_id, self.nid, False, "Cancelled")

        if job.log_config:
            self.setup_logger(job.build_params, job.log_config, target_id)

        printer = self.get_printer(job)
        printer.timedout = False
        printer.cancelled = False

        # Shared Watchdog Timer for both Fill and Print jobs
        watchdog = None
        if job.build_params.timeout is not None:
            def trigger_timeout():
                logging.debug("Timeout triggered")
                printer.timedout = True
            watchdog = threading.Timer(job.build_params.timeout, trigger_timeout)
            watchdog.start()
        logging.debug(f"{printer=}, {watchdog=}")

        try:
            if job.action == 'fill':
                logging.debug(f"Actioning fill for {target_id}")
                res = printer.solve(
                    target_id,
                    stop=job.stop,
                    restart=job.build_params.args.restart
                )
            else:
                res = printer.solve(job.books, cfgid_override=job.cfgid)
        except Exception as e:
            print(f"Exception {job.books[0]}: {e}")
            logging.warn(f"Unhandled error during {job.action} for {target_id}: {e}\n{f_('Traceback: ')}")
            if watchdog:
                watchdog.cancel()
            if self.progress_q:
                self.progress_q.put(ProgressEvent(target_id, 0, "failed", msg=f"Internal error: {e}"))
            raise
            return (target_id, self.nid, False, str(e))

        if watchdog:
            watchdog.cancel()

        if res is None and job.action == 'fill':
            return (target_id, self.nid, f"{target_id} does not exist")

        logging.info(f"Finished {job.action} for {target_id} at {time.asctime()}")
        return (target_id, self.nid, *res) if isinstance(res, tuple) else (target_id, self.nid, res)


_worker_ctx: Optional[WorkerContext] = None

def _init_worker(progress_q, cancel_event):
    global _worker_ctx
    nid = mp.current_process().name
    _worker_ctx = WorkerContext(nid, progress_q, cancel_event)

def _worker_dispatch(job: Job):
    global _worker_ctx
    logging.debug(f"{_worker_ctx=}, {job=}")
    return _worker_ctx.execute_job(job)


class MultiPrint:
    """Multiprocessing scheduler managing job dispatching across worker processes."""

    def __init__(self, numproc: Optional[int] = None, progress: bool = False):
        self.ctx = mp.get_context('spawn')
        self.numproc = numproc or max(1, mp.cpu_count() - 2)
        self.progress_q = GLibCompatQueue(self.ctx) if progress else None
        self.cancel_event = self.ctx.Value('b', False)

        self.executor: Optional[ProcessPoolExecutor] = None
        self.pending_futures: dict[Future, Job] = {}
        self.prev_cpu_times = {}

    def start(self):
        """Start the worker pool."""
        if self.numproc == 1:
            _init_worker(self.progress_q, self.cancel_event)
            return
        self.cancel_event.value = False
        self.executor = ProcessPoolExecutor(
            mp_context=self.ctx,
            max_workers=self.numproc,
            initializer=_init_worker,
            initargs=(self.progress_q, self.cancel_event)
        )

    def _dispatch_job(self, job: Job):
        if self.numproc == 1:
            res = _worker_dispatch(job)
            fut = Future()
            fut.set_result(res)
            self.pending_futures[fut] = job
        else:
            if not self.executor:
                self.start()
            fut = self.executor.submit(_worker_dispatch, job)
            self.pending_futures[fut] = job
        return fut

    def submit_fill_jobs(self, books: list[str], build_params: BuildParams, log_config: Optional[dict] = None, stop: bool = False):
        """Enqueues fill jobs (sorted longest-first) in non-blocking fashion."""
        if not self.executor:
            self.start()
        if self.cancel_event is not None:
            self.cancel_event.value = False

        sorted_books = sorted(books, key=lambda bk: chaps.get(bk, 0), reverse=True)

        logging.debug(f"adding fill for {books}, {build_params=}")
        for bk in sorted_books:
            job = Job(action='fill', books=[bk], build_params=build_params, log_config=log_config, stop=stop)
            self._dispatch_job(job)

    def submit_print_job(self, books: list[str], build_params: BuildParams, cfgid: Optional[str] = None, log_config: Optional[dict] = None) -> Future:
        """Enqueues a print job and returns the Future handle immediately."""
        if not self.executor:
            self.start()

        job = Job(action='print', books=books, build_params=build_params, cfgid=cfgid, log_config=log_config)
        self._dispatch_job(job)
        return fut

    def is_finished(self) -> bool:
        """Non-blocking check to determine if all submitted futures are complete."""
        if not self.pending_futures:
            return True
        return all(fut.done() for fut in self.pending_futures)

    def get_results(self) -> list:
        """Collects results from completed futures and clears pending tasks."""
        if not self.is_finished():
            return []

        results = []
        for future, job in list(self.pending_futures.items()):
            try:
                results.append(future.result())
            except Exception as exc:
                results.append((job.books, None, False, str(exc)))

        self.pending_futures.clear()
        return results

    def start_clock(self):
        self.time = time.time()
        self.prev_cpu_times = {}
        self.total_gops = 0.

    def sample_usage(self):
        freq = psutil.cpu_freq()
        current_ghz = (freq.current / 1000.0) if (freq and freq.current) else 3.0
        processes = getattr(self.executor, '_processes', {})
        tick_cpu_seconds = 0.0
        for pid, proc in list(processes.items()):
            if proc.is_alive():
                try:
                    p = psutil.Process(pid)
                    t = p.cpu_times()
                    total_proc_cpu = t.user + t.system

                    if pid in self.prev_cpu_times:
                        cpu_delta = max(0.0, total_proc_cpu - self.prev_cpu_times[pid])
                        tick_cpu_seconds += cpu_delta

                    self.prev_cpu_times[pid] = total_proc_cpu
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        self.total_gops += tick_cpu_seconds * current_ghz
        return self.total_gops

    def wait(self, timeout:Optional[float] = None) -> list:
        """ Blocks until all jobs finish (or timeout occurs) and returns results. """
        if self.pending_futures:
            wait_futures(self.pending_futures.keys(), timeout=timeout)
        return self.get_results()

    def cancel(self):
        if self.cancel_event is not None:
            self.cancel_event.value = True

    def teardown(self):
        if self.pending_futures:
            for fut in self.pending_futures.keys():
                fut.cancel()
        if self.executor:
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = None
        if self.progress_q:
            self.progress_q.close()
            self.progress_q = None

    def terminate(self):
        """
        Hard stop: Forcefully terminates all worker processes immediately,
        cancels remaining futures, and cleans up queues.
        """
        if self.cancel_event is not None:
            self.cancel_event.value = True

        if self.executor is not None:
            processes = getattr(self.executor, '_processes', {})
            for pid, process in list(processes.items()):
                if process.is_alive():
                    process.terminate()  # Sends SIGTERM to kill worker immediately
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = None

        self.pending_futures.clear()
        if self.progress_q:
            try:
                self.progress_q.close()
            except Exception:
                pass
            self.progress_q = None
