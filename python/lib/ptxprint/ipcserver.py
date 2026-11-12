import gi, re, json, logging, struct
from gi.repository import Gio, GLib
from threading import Thread

logger = logging.getLogger(__name__)

def make_server(view, address, port):
    server = IPCServer(view, address, port)
    res = server.res
    if not res:
        server = IPCClient(address, port)
    return server, res

def _make_packet(obj):
    res = json.dumps(obj, ensure_ascii=False).encode('utf-8')
    return res

def _unpacket(pkt):
    txt = re.sub(r"[\r\n]*$", "", pkt.decode("utf-8"))
    return json.loads(txt)

class _IPCConnection:
    def __init__(self, connection):
        self.connection = connection
        self.instream = connection.get_input_stream()
        self.outstream = connection.get_output_stream()
        self.registrations = {}

    def output(self, pkt):
        res = b"js01" + struct.pack("<L", len(pkt)) + pkt
        logger.debug(f"-->: {pkt}")
        try:
            self.outstream.write_all(res)
        except GLib.GError as e:
            logger.debug(f"-->Failed: {e}")

    def _read(self, n):
        """ n bytes, however many reads it takes; fewer only at the end of the stream """
        res = b""
        while len(res) < n:
            dat = self.instream.read_bytes(n - len(res), None).get_data()
            if not dat:
                break
            res += dat
        return res

    def read_pkts(self):
        while True:
            hdr = self._read(8)
            if len(hdr) < 8:
                break
            if hdr[:4] != b"js01":
                logger.debug(f"--< not a PTXprint packet: {hdr}")
                break
            datlen = struct.unpack("<L", hdr[4:8])[0]
            indat = self._read(datlen)
            if len(indat) < datlen:
                break
            logger.debug(f"--<: {indat}")
            yield indat

class IPCServer:
    def __init__(self, view, address, port):
        self.view = view
        self.max_threads = 4
        self.connections = []
        self.res = False
        self.thread = Thread(target=self.make_server, args=(address, port))
        self.thread.start()
        self.thread.join(1.0)

    def make_server(self, address, port):
        self.server = Gio.ThreadedSocketService.new(self.max_threads)
        try:
            self.res, _ = self.server.add_address(Gio.InetSocketAddress.new_from_string(address, port),
                             Gio.SocketType.STREAM, Gio.SocketProtocol.TCP, None)
        except GLib.GError as e:
            self.res = False
            return
        self.server.connect("run", self.do_run, None)

    def transmit(self, regkey, obj):
        pkt = _make_packet(obj)
        for c in self.connections:
            if regkey is None or regkey in c.registrations:
                c.output(pkt)

    def do_run(self, server, connection, src, dat):
        conn = _IPCConnection(connection)
        self.connections.append(conn)
        try:
            for pkt in conn.read_pkts():
                try:
                    dat = _unpacket(pkt)
                    verb = str(dat['verb']).lower()
                    params = dat.get('params', [])
                except (ValueError, KeyError, TypeError, AttributeError) as e:    # not JSON, or no verb
                    logger.debug(f"--< bad packet {pkt}: {e}")
                    continue
                fn = getattr(self, "verb_"+verb, None)
                if fn is not None:
                    fn(conn, *params)
        except GLib.GError as e:
            logger.debug(f"--< connection failed: {e}")
        finally:
            self.connections.remove(conn)       # closed: don't send to it any more

    def verb_project(self, conn, prjid=None, cfgid=None, *a):
        self.view.onIdle(self.view.setPrjConfig, prjid, cfgid)

class IPCClient:
    def __init__(self, addr, port):
        # import pdb; pdb.set_trace()
        self.client = Gio.SocketClient.new()
        connection = self.client.connect_to_host("{}:{}".format(addr, port), port, None)
        self.connection = _IPCConnection(connection)
        self.rdr = None

    def transmit(self, obj):
        pkt = _make_packet(obj)
        self.connection.output(pkt)

    def expect(self):
        if self.rdr is None:
            self.rdr = self.connection.read_pkts()
        pkt = next(self.rdr)
        dat = _unpacket(pkt)
        return dat


