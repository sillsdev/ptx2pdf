# Developer to-do

Problems found along the way that are outside the work in hand. Add to the
end; remove an item when it is fixed.

## Page filler

* **Polyglot: evening a crossing slice ignores notes (to do).** aArp TestDiglotA5 MAT
  p50 (10:21-23, 1 line gap in Tok Pisin above v24). Filling p49 stretched Arop's
  10:21 paragraph by 1 into a 1 line gap at the foot of Arop's column (the next Arop
  line, "22 ...", could not move up: its 10.22 notes would not fit). Evening the slice
  end on p50 then undid that +1, predicting a line pulled back from p50; instead p49
  went short again and p50 was unchanged. `balance_crossing` should not predict that
  shrinking pulls back a line that carries a note caller. Tried and rejected: never
  shrinking a paragraph below the shape the page's fill gave it (fixed p50 but made
  p45 a 4 line gap and cost +22% runs on MAT 1-11). Repro: `fill -b "MAT 1-11"`
  (needs fill-chapter-range.patch), ~4 min.
* **Fill with a chapter range rewrites the whole adjlist.** `fill -b "MAT 1-11"` writes
  the book's adjlist with only those chapters' entries (a full fill also rebuilds it).
  Keeping the other chapters' entries is more work than it is worth for now.

* **Polyglot: whole-book slice balance pass after filling (to do).** After
  the pages are filled, some slices are still not optimally balanced. Add a
  pass over the whole book, not page by page, that fixes every unbalanced
  slice without changing its height, so page breaks are not disturbed.
  Assume 1 or 2 passes over the book are enough. (Today balancing happens
  only per page while filling: `balance_page`, `balance_crossing`.)
  aArp TestDiglotA5 MAT fill (2026-10-28, weight 1, no 105%+2 probe): 105 of
  680 slices are 2+ lines out. Wholly on a page: 34 have shapes that would fix
  them at 10–20 badness a line (weight 1 = 10, so not taken), 30 have the
  short glot already at its largest shape (9 of those with the long glot
  stretched), 1 fixable at weight 1. Crossing a page: 27 fixable at weight 1
  but never tried (`balance_page` skips crossing slices), 5 at weight 2, 8 no
  shapes.
* **Diglot: a page-wide picture that fits the space left but not with its
  slice's text still cuts a glot at its anchor.** aArp MAT p7: the 2:11 top
  picture (`gt00021`, 274pt, anchored at 2:12) is tested against `\availht`
  289pt at the slice start, so `diglot-defer-page-picture` doesn't defer it.
  Trials that reach the anchor then fail, aArp breaks before it with ~11 empty
  lines at the foot of p7, and its last 6 lines go to p8 under the picture.
  The test needs the slice's text up to the anchor counted as well.
  *Addressed in the working tree (patches/diglot-trial-holdover.patch, not yet
  applied):* trials keep `\count`=1000 so TeX holds the picture over. Two
  follow-on fixes: `\skip\topins`/`\bottomins` cancel the pictures already
  on the page during a trial, or TeX counts them twice (p12: 3:16 went
  whole to p13); `\d@rerun@trial` recomputes `\availht` after the failed try's
  inserts are restored (p26: one slice, then 450pt empty).
* **Diglot: a picture held over from the book's last page is lost.** The
  next-page store (`save<ins>nxtpg`) is only restored after a diglot
  shipout, but at book end `\enddigl@t` hands `\partial` to the normal output
  routine. Seen in aArp MAT printed with the 28 Oct fill's adjlist plus the
  fixes above: the 28:20 picture (421pt) is missing (57 of 58 placed). The
  store needs flushing at book end, onto a page of its own if need be.
* **`badness_modify` applies the expansion terms only when the rag
  (`parbadness`) is at most 0.1**; otherwise badness is just whiteness plus
  rag, and the rag is in points while whiteness is relative to the text size.
  Worth checking this is intended.
* **One early failed page switches repair off for the rest of a book.**
  `TypesetterSolver.run_forward` only repairs when
  `failed_pages[0] > low_water`; `failed_pages[0]` is the first page that
  ever failed and `low_water` only rises, so after e.g. an unfillable opening
  page no later page is ever backtracked. Testing instead "no failed page in
  `[low_water, page)`" made repair run again (WSGlatin RUT diglot: 9 page
  attempts became 146) but filled nothing more and took 1000s instead of 60s,
  so it needs a cost limit as well before it is worth changing.

* **my_judson Diglot_BSB, Jonah fails to typeset**, as a plain print as well
  as a fill: "Improper state; '' should be 'L' 'R' ... Maybe there was output
  before columns were set up?". Probably something in the merged file before
  the first `\polyglotcolumn`.

* **Diglot lost-data safety net.** `\@lostdata{ref}{glot}{where}` in the parlocs now marks text
  TeX could not place (trial met by a column switch, or collect with no column); the parlocs
  reader drops those paragraphs, so the filler sees them as unmeasured. A layout that lost
  text (`Paragraphs.lostdata`) is not yet held against it when the solver accepts it.
* **Polyglot fill of WSGlatin Triglot2JN fails on page 2.** Its layout has no `\@Poly@colstart`
  records, so the filler has no baselines (it now falls back and fills, page 2 failing).
  (projects/IT2 diglot MRK failed because MVE has no MRK: now reported as that.)

## Headless crash testing (Oct 2026)

* **XFAILs in the sandboxed test environment.** WSGdev/Guides and other
  configs differ from their standards here even without any lib changes. In
  Guides the standard embeds AnnapurnaSIL-Bold, but the output uses a fake
  (emboldened) regular, as the config asks. Worth checking whether the
  standards or the font lookup are out of date.

### Configs that could be pruned (not done)

* WSGdev `Intro-NO-Outline`, `NOintro-NO-Outline` and `Nointro-NO-Outline`
  (and their standards) are untracked case variants of the tracked
  `Intro-NO-OutLine` and `NOintro-NO-OutLine`. They look like leftovers from
  mistyped `-c` names, but the suite runs them because they exist.
* WSGdev `Guides` and `GuideWithCropMarks` differ only in `ifcropmarks`.
  `Grid2EdgeOfPage` and `Grid2EdgeOfPageWithCropMarks` differ in crop marks
  and in which side the header goes. One of each pair would do; crop marks
  are also covered by WSGlatin `Impose2JN`.
* `test/standards/WEBorig/WEBorig_Long_GEN_ptxp.pdf` is stale: Long now
  prints GEN–GLO, and its standard is 13MB.
* The configs with standards over 1MB (aArp TestDiglotA5, OGNT Long,
  OGNT Diglot-FullNT, WEBorig Long, WSG Strongs) now only run with `--slow`.
  WSGlatin `Diglot2JN`, `Triglot2JN` and the in-process diglot fuzz cover
  diglot crash paths quickly.

## GUI tests and archives (Oct 2026)

* **Old GUI test recordings need re-recording.** Recordings made before
  gtktest-harness.patch hold `tv_Styles` row paths, which depend on the tree's
  filter and contents, and `___object_NNN___` widget names, which aren't
  stable. `projects/_PTXprint/BSB_1/local/ptxprint/Test_simpleedits_nosave.zip`
  fails for this reason. A copy with the markers filled in by hand passes.
* **Archives: things still not handled.**
  - A diglot's other project resolves its sidebar images against its own
    working directory, but TeX runs in the main project's.
  - Only modules the process script imports by name from beside it are
    archived; data files it opens, or packages, are not.
  - TeX in ptxprint-mods.tex that builds file names with macros
    (`\input\mypath/x`) can't be followed.
* **Recordings include PTXprint's own reactions.** A change PTXprint makes in response to the
  user (e.g. `s_indentUnit` after turning off two columns, `ecb_savedConfig` after Save as) is
  recorded as if the user did it. Replays set the same values, so tests pass, but tutorials show
  them as steps.

## Bug hunt (Nov 2026)

Found by reading the code (with the todo-*.patch series applied), plus small headless tests
where noted "tested". Line numbers are as of those patches. Most severe first in each group.

Status: each item starts with **[FIXED patches/X.patch]** (fixed in that patch, not yet
committed), **[NOT A BUG: why]**, or **[OPEN: why]** (looked at, deliberately left). No tag =
not looked at yet.

### Config, model and TeX generation

* **[FIXED patches/bugs-config.patch]** `view.py:1674` `loadConfig` looks for section `strongsvar`, but `createConfig` writes
  `strongsvars`: Strong's index titles are lost on load and dropped on the next save (tested,
  WSGBTpub BellsAndWhistles). Loading them then showed `gtkview.setvar` writing a
  publishable column the Strong's list doesn't have (IndexError) — also fixed.
* **[FIXED patches/bugs-config.patch]** `view.py:798-823` `_mergetxt` loops forever when one side deleted a line and the other added
  one (copy config to other projects with "merge") (tested).
* **[FIXED patches/bugs-config.patch]** `ptsettings.py:236-238` `calcbookspresent`: off by one book, and `bkcode=v+1` is an int, not
  the zero-padded code, so BooksPresent is wrong (WSGlatin: OBA TIT HEB... instead of RUT JON
  PHM...) and is saved to ptxSettings.xml (tested).
* **[FIXED patches/bugs-config.patch]** `modelmap.py:27` `transparency_` tests for `"PDF/X-4"`, which is no longer an output format
  value, so `\NoTransparencytrue` is on for every format, including Screen.
* **[FIXED patches/bugs-config.patch]** `adjlist.py:73-79` `find` compares a UserList slice with a tuple (never equal), so
  `setval(append=False)` adds a duplicate row instead of updating; `cleanup` (216-226) compares
  `lastk`, which is never updated, so duplicates are never removed (and `remove(lastk)` would
  pass a list). The page filler relies on this path (tested).
* **[FIXED patches/bugs-config.patch]** `adjlist.py:320` an inserted row gets expand 100 whatever the font's `extend` centre.
* **[FIXED patches/bugs-config.patch]** `adjlist.py:269` `remove_file` calls `self.model.statusMsg`; AdjList has no `model`.
* **[FIXED patches/bugs-config.patch]** `adjlist.py:111` the `force` branch puts a str in `db`; `genline` would crash (no callers).
* **[FIXED patches/bugs-config.patch]** `snippets.py:170-177` the `else` of the Gray test sets `_iccnumcols` to 4, so Screen/Digital
  PDFs declare the sRGB profile as `/N 4`.
* **[FIXED patches/bugs-config.patch]** `snippets.py:293-325` FancyBorders formats the whole text after the loop with the last
  glot's dict: diglot L gets R's section head and page border settings.
* **[FIXED patches/bugs-config.patch]** `snippets.py:521` stray `print(f"{mwidth=}")` on every print with margin notes.
* **[FIXED patches/bugs-config.patch]** `texmodel.py:568` `_addLR`: missing comma joins `\isodate` and `\book`, so neither gets its
  L/R form in diglot headers.
* **[FIXED patches/bugs-config.patch]** `texmodel.py:903` front matter picks CMYK images only for CMYK/PDF-X-1A/PDF-A-1, not
  Transparent or Spot.
* **[FIXED patches/bugs-config.patch]** `texmodel.py:638-640` `prep_pdfs` on Windows: `C:\...` survives the `/`→`_` replace, so the
  output path is the source and front/back PDFs are never sanitised.
* **[FIXED patches/bugs-config.patch]** `texmodel.py:1757` with `xrefs.py:127`: custom xref list copyright never printed
  (`.lower` without `()`, and read from the TexModel instead of the xrefs object).
* **[FIXED patches/bugs-config.patch]** `view.py:1790-1796` `saveAdjlists` returns nothing, so saveConfig resets ptxprint.cfg's
  mtime even when adjlists changed.
* **[FIXED patches/bugs-config.patch]** `view.py:1948/1952` `get_adjlist` falls back to `self.expand`, which ViewModel lacks
  (AttributeError on a non-numeric shrink/stretch limit).
* **[FIXED patches/bugs-config.patch]** `view.py:755` `_copydir` replaces the config name anywhere in a file name (config `lat` in
  project WSGlatin renames `...WSGlatin-lat...` wrongly).
* **[FIXED patches/bugs-config.patch]** `view.py:769-781` `_mergecfg` only walks the target's sections; sections only in the source
  ([vars], [publication.X], [diglot_R]) are not merged.
* **[FIXED patches/bugs-config.patch]** `view.py:1000-1004` a project picCopyrights.json replaces whole sub-dicts (shallow update),
  losing the built-in artist codes.
* **[FIXED patches/bugs-config.patch]** `view.py:229-241` `setDate` uses `time.daylight` (zone has DST) rather than DST in effect:
  winter PDF dates get the summer offset (tested, Europe/London).
* **[FIXED patches/bugs-config.patch]** `view.py:1308/1367` upgrades from < 2.09: PDF/X-1A from < 1.7 becomes Screen (checks
  `snippets/` not `document/pdfoutput`), and section `finish` vs `finishing` resets
  pgsperspread.
* **[FIXED patches/bugs-config.patch]** `ptsettings.py:359-363` `parsebook` looks up `bk.lower()` in case-sensitive bkNames:
  "Jonah" is an illegal book name (tested, WEBorig).
* **[FIXED patches/bugs-config.patch]** `ptsettings.py:109` writes misspelt key `DeafultFontSize`.

### Print job, filler, parlocs, merge, PDF

* **[FIXED patches/bugs-printjob.patch]** `parlocs.py:765-768` `getnbadspaces`: iterates the 3-tuple from `has_badspace` as if a list
  of triples, and adds undefined `nspace`. Crashes layout analysis in the viewer (threshold 0)
  and the report (runjob then deletes the HTML report quietly) (tested).
* **[FIXED patches/bugs-printjob.patch]** `runjob.py:1318-1330` CMYK image conversion: uint8 `img[:,:,3] + dk` wraps, so the `>255`
  mask never fires and rich black becomes ~40% grey; the mask branch uses `255-dk` for
  `255-k`; the 3-channel branch calls `img.concatenate` (no such method) with axis 3 (tested).
* **[FIXED patches/bugs-printjob.patch]** `main.py:725` with `multiprint.py:384`: a failed fill job reports `job.books` (a list), and
  the results sort does `bookcodes.get(list)` → TypeError; the whole summary is lost.
* **[FIXED patches/bugs-printjob.patch]** `bookProgressDlg.py:137-146` with `page_filler.py:1434`: only "badpage" events mark a
  failure; poly_filler sends no ProgressEvents and the final event's "Failed from N"/"Timed
  out" message is ignored, so failed polyglot fills show green "Complete".
* **[FIXED patches/bugs-printjob.patch]** `multiprint.py:291` worker folders named after `mp.current_process().name` pile up
  (projects/ has pbuildSpawnProcess-1..30, ~100MB), two ptxprint processes share names (and
  clear each other's files), and terminate() leaves xetex children running.
* **[FIXED patches/bugs-printjob.patch]** `runjob.py:1350-1381` `carefulCopy` returns the target name even when the copy/convert
  failed, so a broken image is never "missing": TeX fails even with "omit missing pictures".
* **[FIXED patches/bugs-printjob.patch]** `usfmerge.py:1224-1240` merge config path is dirname^3 of the input: in a worker folder
  (pbuildX) it misses `shared/ptxprint/<cfg>/merge-*.cfg`, so fills ignore a custom merge cfg.
* **[FIXED patches/bugs-printjob.patch]** `usfmerge.py:1103-1105, 1217-1221` merge `settings` flags are a module global that scores
  mode and custom cfgs change and never restore: later merges in the session differ.
* **[FIXED patches/bugs-printjob.patch]** `usfmerge.py:1256` `searchlist.extend((path, 0))` should be `append`.
* **[FIXED patches/bugs-printjob.patch]** `parlocs.py:496` `currp` isn't cleared at `@parlen`, so a picture after a finished paragraph
  adds a rect to it; the filler then thinks it continues onto the picture's page (tested).
* **[FIXED patches/bugs-printjob.patch]** `parlocs.py:632` `getParas(inclast=True)`: `self[start:-1:-1]` is always empty; clicking
  the continuation of a paragraph at a page top gives no reference. `setFigPids` (690) is also
  broken (no callers).
* **[FIXED patches/bugs-printjob.patch]** `parlocs.py:666, 818` last page skipped / pages off by one in `getParasByColumnOrParref`
  and `getstats`.
* **[FIXED patches/bugs-printjob.patch]** `pdf/procpdf.py:108` a ValueError from fixpdffile returns `{}` silently and runjob.procpdf
  always returns True: CMYK/spot/burst output silently not made. Lines 188/202 read
  `kw["pdfdate_"]` but runjob passes `date`, so PieceInfo LastModified is "D:".
* **[FIXED patches/bugs-printjob.patch]** `multiprint.py:316-337` with numproc 1 (2-core machines) jobs run in the GUI thread: UI
  freezes, Stop/progress don't work, basicConfig(force) redirects the GUI's logging, cwd is
  left in pbuildMainProcess, and a worker exception stops the remaining books.
* **[FIXED patches/bugs-printjob.patch]** `multiprint.py:61, 90` `logger` and `re` not imported; line 92 precedence gives `bks=""`
  for a single book.
* **[FIXED patches/bugs-printjob.patch]** `runjob.py:723-731` `communicate()` has no timeout: `s_pbtimeout` and Stop can't stop a
  running xetex.
* **[FIXED patches/bugs-printjob.patch]** `runjob.py:753` a xetex killed by a signal (negative returncode) isn't a failure.
* **[FIXED patches/bugs-printjob.patch]** `runjob.py:982` xdvipdfmx log opened without encoding (UnicodeDecodeError on Windows).
* **[FIXED patches/bugs-printjob.patch]** `runjob.py:197` early return in `doit` (no project id) without `unlockme()`: every later
  print says busy. Line 253: `digcfg.captions` on None when polyglots lacks the view.
* **[FIXED patches/bugs-printjob.patch]** `runjob.py:465-475` `digdojob`: unguarded `convertBook` (None → TypeError), `texfiles`
  undefined if every view is skipped, `project/bookids` and `project/books` misaligned for a
  module.
* **[FIXED patches/bugs-printjob.patch]** `page_filler.py:655` `lpars[-1]` IndexError on a page with no paragraphs (full-page picture).
* **[FIXED patches/bugs-printjob.patch]** `page_filler.py:414` inverted conditional → `range(None)` (only with start_page > 0).
* **[FIXED patches/bugs-printjob.patch]** `page_filler.py:1745` `read_badnesses` uses unimported `SpacingOddities` (no callers).

### GUI (gtkview and friends)

* **[FIXED patches/bugs-gui.patch]** `gtkview.py:2645-2652` Print with "process script" ticked and no script: `os.lstat(None)`
  TypeError (FileNotFoundError if the script moved); the spinner keeps going.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:5476-5482` importing settings from `X.PDF` (upper case) goes to ZipFile →
  BadZipFile; dialog left open.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:6371` `.get_sensitive` without `()`: OK on the DBL import dialog with no bundle →
  `ZipFile(None)`.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:4353-4361` cancelling the multi-book chooser switches the scope to single.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:6526-6531, 6551-6556` Esc/X leaves dlg_overlayCredit and dlg_sbPosition shown
  but dead.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:3805-3810` with `tatweel.py`: the dialog is never reused (checks
  `tatweel_dialog`, stores `dialog`), so each opening adds handlers and another 1s timer;
  closing with X leaves timers writing to destroyed widgets; `logger` undefined in tatweel.py.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:3466-3475` Generate on the Final SFM tab for a book not in scope:
  `convertBook(None)` TypeError. `3461-3463` Esc on "Adjust lists already exist" still
  generates.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:3613-3633` `onViewerChangePage`: `or`/`and` precedence → `bks[0]` IndexError
  with no books; FinalSFM `os.path.join(..., None)`; early return leaves `noUpdate` True,
  silently stopping book-change and font/baseline lock handlers.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:2589-2672` early returns in onOK ("no books", missing fonts, PDF locked,
  callback exception) leave the busy spinner running.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:5246-5327` Cancel in the script / xref file / module choosers clears the
  existing setting (and unticks process script / switches to single book).
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:781-789` `_dlgtriggers` keys `dlg_multiBookSelect`, `dlg_multProjSelector`,
  `dlg_gridsGuides` don't match the glade ids, so search can't open those dialogs (and
  `adjustGridSettings` needs two args).
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:4618` black text colour test compares with `"x000000"`, never `"#000000"`, so
  black turns on coloured fonts.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:3901-3904` saving an emptied editor buffer writes nothing (old contents
  return); 3897 `adjView.adjlist.save()` with no adjlist → AttributeError.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:7684-7795` cancelling Add Map leaves `XXM mapNN` piclist entries with no anchor.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:5655` `basedir is not None or not basedir` (should be `and`); 5262 xrf filter
  `"patterns": "*.xrf"` is a string, added a character at a time, so it shows every file.
* **[FIXED patches/bugs-gui.patch]** `gtkview.py:4115` `onEditStyleClicked` as `activate-link` handler returns None, so GTK tries
  to open each link's text as a URI (warning per click).
* **[FIXED patches/bugs-gui.patch]** `gtkview.py` minor: `dlg_fillProgress` not in glade (no parent); `btnUnpackClicked` refers to
  missing widgets (no callers); `onSaveEdits` uses `pg` before assignment; `resetParam`
  connected to a bare GtkLabel (`l_styRaise`) has no `get_child()`.
* **[FIXED patches/bugs-gui.patch]** `gtkadjlist.py:59-66` deleting rows removes them from the liststore but not `adjlist.db`, so
  later rows get the wrong trig/shape comments when saved (tested). `gtkadjlist.py:33` edits
  to the Parameters column are ignored on save; editing Para breaks the sort `changeval`
  relies on.
* **[FIXED patches/bugs-gui.patch]** `pdf_viewer.py:146-155` `__getattr__` falls back to `self.views` (it's `viewers`) and returns
  None instead of raising: toggling overlays with the Cover/Diff tab current → TypeError.
* **[FIXED patches/bugs-gui.patch]** `pdf_viewer.py:2264-2280` `hitPrint()` only in the 'col' branch of Frame Size: page/full/span
  don't auto-update.
* **[FIXED patches/bugs-gui.patch]** `pdf_viewer.py:965-971` print_document: UnboundLocalError after an exception; there and at
  539/1100 `_("...: ").format(e)` has no `{}`, so the error text is dropped.
* **[FIXED patches/bugs-gui.patch]** `pdf_viewer.py:1878-1898` a right-click within the auto-update delay cancels a pending
  update for good.
* **[FIXED patches/bugs-gui.patch]** `pdf_viewer.py:174-182` `onPageChanged` puts the page index in `t_pgNum`, which is read as a
  folio: jumps to the wrong page with front matter.
* **[FIXED patches/bugs-gui.patch]** `pdf_viewer.py:1635-1653` the "Analysing text" dialog stays up if parsing raises.
* **[FIXED patches/bugs-gui.patch]** `report.py:66-68` every Report adds a root logging handler, never removed: N prints → each
  log line printed N times and memory grows; `Report.clear` never called, so the runtime
  section has every message since startup.
* **[FIXED patches/bugs-gui.patch]** `gtkpolyglot.py:57-59` query-tooltip connected 11 times (inside the column loop).
* **[FIXED patches/bugs-gui.patch]** `gtkpolyglot.py:396-470` changing a new row's code A→B: `createDiglotView` raises inside
  the handler; for a configured row an extra ViewModel is built and thrown away.
* **[FIXED patches/bugs-gui.patch]** `main.py:241` `--timeout` parsed but never used. `main.py:624-726` `-P -B` and `fill` always
  exit 0.
* **[FIXED patches/bugs-gui.patch]** UI language "ar_SA.UTF-8" (from LANG, or after switching language) never equals `'ar_SA'`
  (pdf_viewer 791/921/1705/1809, gtkstyleditor 686, gtkview 2320): RTL navigation buttons
  swapped twice, translated help links unused.
* **[FIXED patches/bugs-gui.patch]** `ipcserver.py:37-81` short reads not handled, missing 'verb' → KeyError, closed connections
  kept, magic never checked.
* **[FIXED patches/bugs-gui.patch (the GLib critical); OPEN: auto-closing errors after 30s unread looks deliberate — your call]** `gtkutils.py:263-268` doError: `source_remove` on an already-removed timer (GLib critical);
  error dialogs close unread after 30s.
* **[FIXED patches/bugs-gui.patch]** `picselect.py` ImageSet (moved out of gtkview): `Pango`, `urllib`, `rmtree` not imported,
  `self.project`/`onGetPicturesClicked`/`onHideStatusMsgClicked` belong to `self.view`; the
  image set dialog fails as it opens. `TagableRef.asint` uses undefined `books`/`vrs`.

### Pictures, styles, fonts, text processing

* **[FIXED patches/bugs-text.patch (pictures before verse 1, anchored at the verse after them, where TeX places them); OPEN: intro pictures — TeX has no verse to anchor them to and I couldn't confirm its paragraph reference in an intro]** `piclist.py:615` `"(.*?)\\v "` is a vertical tab to the regex: pictures before verse 1 of a
  chapter are never read; the intro block (no `\v`) is lost even when fixed (tested).
* **[FIXED patches/bugs-text.patch]** `piclist.py:908` `merge_fields` calls `Picture.update` (doesn't exist): importing chosen
  picture fields crashes (tested).
* **[FIXED patches/bugs-text.patch]** `piclist.py:334` `getattr(self, 'pgpos')` is always None (fields are in `self.fields`), so
  GLO `pgpos="p"` and USFM2 positions are overwritten in two-column layouts (tested).
* **[FIXED patches/bugs-text.patch]** `piclist.py:573` attribute regex `[a-z]+?=` drops hyphenated names' prefix: `x-credit` stored
  as `credit`, `x-xetex` as `xetex` (tested).
* **[FIXED patches/bugs-text.patch]** `piclist.py:370` `(\d+(?:\.\d*))` needs a decimal point: `size="col*2"` loses its scale.
* **[FIXED patches/bugs-text.patch]** `xrefs.py:441-461` Strong's renderings: multi-word renderings never match (no `\s+`), `a/b`
  doesn't match `b a`, `*`/`**` lack separators (tested).
  → The WSG-Strongs standard now differs (xfail): Strong's numbers in JHN now attach where
  two-word renderings match. Update the standard once you've checked it.
* **[FIXED patches/bugs-text.patch]** `xrefs.py:386` prefix/suffix swapped in `merge`; `WordForm.merge` (39/43) `.add` on None.
* **[FIXED patches/bugs-text.patch]** `xrefs.py:136` a blank line in an .xrf → IndexError (tested). `xrefs.py:198` `BaseBooks`
  undefined; no `strongsfilter` for non-Strong's XML lists.
* **[FIXED patches/bugs-text.patch]** `xrefs.py:557-558` sets `parent.hasLocalBookNames` not `parent.ptsettings...`, so book names
  are rebuilt every time; writes `bookNames`, which nothing reads.
* **[FIXED patches/bugs-text.patch]** `usxutils.py:270-296` `makeBookNames` \toc fallback loops over an always-empty list; if
  fixed, `while nochap` loops forever on a book with no `\c`; reads as UTF-8 whatever the
  project encoding. `usxutils.py:600` `normalise` uses undefined `canonicalise`.
* **[FIXED patches/bugs-config.patch]** `utils.py` `cachedData` (xref files): cache keyed by basename + version only, so edits to a
  custom xref file are ignored and same-named files in two projects share a cache.
* **[FIXED patches/bugs-text.patch]** `utils.py:759` `special_regexes['BA']` missing `]` (tested). `utils.py:955`
  `UnzipDir.infolist` uses unimported `ZipInfo` (archive import from a folder).
* **[FIXED patches/bugs-text.patch]** `changes.py:192` `#` inside a quoted string is taken as a comment (tested).
* **[FIXED patches/bugs-text.patch]** `changes.py:220-221` a bad `at` reference applies the rule to every book (tested).
* **[FIXED patches/bugs-text.patch]** `changes.py:230/232` `at GEN 1-2` only applies to chapter 1 (`r.chapter` for `cr.chapter`)
  (tested).
* **[FIXED patches/bugs-text.patch]** `changes.py:127` `\p{mkr=para+char}`: `+` tests the wrong list and subtracts (tested).
* **[FIXED patches/bugs-text.patch]** `unicode/ducet.py:64, 87, 237` implicit/fallback/tailored weights stored as bytes, not
  tuples: sort keys crash for CJK and unlisted characters (TOC sort, Strong's reversal) (tested).
* **[FIXED patches/bugs-text.patch]** `unicode/UnicodeSets.py:179` `flatten` advances before its first yield: `[abc]` →
  `['b','c']`, `[a-c]` → `['b']`; the LDML index letters (Strong's index) lose entries.
  `_expand` uses undefined `indices` (tested).
* **[FIXED patches/bugs-text.patch]** `unicode/ucd.py:213` `isnormalized` test inverted (`normal_ucd("é","NFD")` unchanged).
* **[FIXED patches/bugs-text.patch]** `font.py:268` `addFontDir` skips `.otf`.
* **[FIXED patches/bugs-text.patch (all but iscore); OPEN: `iscore = True` before its test looks deliberate — your call]** `font.py:1158, 1219` `copy`/`fromStyle` drop `lang`. `font.py:1098` 3-field config →
  UnboundLocalError. `font.py:168` `parseFeatString("smcp=1, liga = 0")` ValueError (tested).
  `font.py:1201` calls nonexistent `readFeats()` for `/GR` styles; `to_dict` (1095) stores
  `lang` under 'feats'. `font.py:1276` sets `iscore = True` just before testing it (project
  fonts always referenced by name; maybe intended).
* **[FIXED patches/bugs-text.patch]** `hyphen.py:190-196` Hunspell: `__init_`, `Dictioanry` typo, undefined `Dictionary` — the
  spylls path can never work.
* **[FIXED patches/bugs-text.patch]** `dbl2ptx.py:236` tries UTF-16 before cp1252, so legacy cp1252 files decode as garbage.
* **[FIXED patches/bugs-text.patch]** `dbl.py:40` BookNames.xml attribute values not escaped (`&`, `"`).
* **[FIXED patches/bugs-text.patch]** `borderstyle.py:128` inner/outer borders round-trip as left/right ("All").
* **[FIXED patches/bugs-text.patch]** `imagestyle.py:158` `removeStyle` removes keys that never exist, leaving `Bg/FgImageScale`.
* **[FIXED patches/bugs-text.patch]** `interlinear.py:166` `int("12a")` for subverse refs.
* **[FIXED patches/bugs-text.patch]** `project.py:235` `shareConfig` uses unimported `copytree`.
* **[FIXED patches/bugs-text.patch]** `pdf/pdfsig.py:46` `isinstnace` typo. `pdf/pdfinish.py:218` `scale_to_fit` from another
  method (NameError). `xdv/xdv.py:131` `uint=unit` (NameError for 3-byte values), `245` `os`
  not imported (diffable mode). `xdv/layout.py` uses undefined `XDViPositionedReader` and bare
  `lspace` (module unusable). `xdv/colouring.py:188` `proc` undefined in `main`.

### TeX macros

* **[FIXED patches/bugs-tex.patch]** `ptx-stylesheet.tex:2237` `\ifnum\pagetotal>0pt`: a dimension in `\ifnum`, so "pt" is
  typeset when a book ends on the page it started with material on it (tested construct).
* **[FIXED patches/bugs-tex.patch]** `ptx-output.tex:2362-2371` three-column trial tests the two-column flag
  (`\ifrerunsavepartialpaged`; `...paget` is set but never tested) and installs undefined
  `\savepartialpagetounce` (for `...tbounce`).
* **[FIXED patches/bugs-tex.patch]** `ptxplus-marginalverses.tex:11` redefines `\getnum` (ptx-figure.tex:302's): with marginal
  verses on, `x-xetex="rotate=odd=42"` errors.
* **[FIXED patches/bugs-tex.patch]** `ptx-char-style.tex:458` `\let\shdw@y\shdw@x` should be `\@@shdw@y`/`\@@shdw@x`: a
  one-value `\Shadow` errors.
* **[FIXED patches/bugs-tex.patch]** `ornaments.tex:109-110` `\ifx\dimen1=0pt` (should be `\ifdim`) and undefined
  `\@notpgfornamentdim`.
* **[FIXED patches/bugs-tex.patch]** `ptx-tables.tex:390, 396` `\l@ftbal` undefined (it's `\l@ftb@l`): LeftBal rows unbalanced.
* **[FIXED patches/bugs-tex.patch]** `ptx-para-style.tex:638` `\thisp@rcl@ss` typo (for `\thisp@rclass`): `\lastp@rclass` never
  updated, so in a sidebar a heading after paragraphs loses its space before.
* **[FIXED patches/bugs-tex.patch]** `ptx-attribute.tex:170` `\pdfURL` tests undefined `\@GOTOLinkBorderCol` (for
  `\URLLinkBorderCol`): an empty colour still writes `/C[]`.
* **[FIXED patches/bugs-tex.patch]** `ornaments.tex:1673` doubled `\ifx` in `\zSEQ`: the `\orn@Side`=`\relax` fallback never fires.
* **[NOT A BUG: \\SSsetLRspecific and \\triallist are gone already; the gridone joint calculation has no caller (dead, harmless)]** `ptx-diglot.tex:232-233` `\SSsetLRspecific` uses undefined `\@orig`, `\pr@cessSpecific`
  (no callers). `3894` `\triallist` for `\tri@llist` (harmless). `2009-2030` gridone joint
  calc needs undefined `\diglotgridcolumn` (dead).
* **[OPEN: features without a UI setting (settable from ptxprint-mods.tex): add UI or remove — your call]** Flags nothing sets: `\ifdiglotSwap` (setter commented out in snippets.py:208),
  `\ifDgltHdrOffsetCenter`, `\ifreftooltip`.
- **[OPEN: TeX never sees unknown markers like \\zunknown, because Python drops them in the conversion; undefined milestones (and \\u0000) get through. The fix belongs there: drop and warn as for other unknown markers]** Undefined markers kill TeX with a bare "Undefined control sequence" instead of a helpful message: a milestone with no stylesheet entry (`\zcustom-s |who="x"\* … \zcustom-e\*`), and `\u0000` (marker name followed by digits). `\zunknown …\zunknown*` and `\xyz` are fine. Found when OddUSFM's JUD started reaching TeX (usfmtc e72a391); taken out of the test data in patches/oddusfm-cleanup.patch.
- **[OPEN: not looked into further (the test data was cleaned instead)]** Unclosed `\f` running into an unclosed `\fig` ends in "Argument of \getonep@ram has an extra }" — no hint of the real cause (also cleaned out of OddUSFM).

## Hidden bugs (Nov 2026, second pass)

Found by a deeper read than the bug hunt above. Same status tags; no tag = not looked at yet.

### Multi-project manager

* `manager/validate.py:138` `bookIsEmpty` counts only the text between `\v N` and the next
  backslash or line end. A verse that starts with a character style (`\v 1 \w In|strong="G1722"\w* ...`),
  a footnote, or that puts its text on the next line after `\q1` counts 0 words, so a translated
  book with Strong's markup, or poetry (PSA), is reported as the ERROR "bookEmptySecondary" and
  test-print failures are blamed on it (`testprint.py:151`) (tested: three such verses count 0).
  Count words in the whole chapter text with markers and attributes stripped instead.
* `manager/testprint.py:82-95` Stop races with a print that is starting: `stop()` kills only the
  processes already in `self.processes`, so a `Popen` made between the `stopping` test and
  `processes.add` runs to completion (up to the 900s timeout) after Stop, and is then reported as
  "Stopped". Test `stopping` again after adding the process (traced, not run).

### Page filler and layout analysis

* `adjlist.py:366-369` `increment`: a `+N` value that goes negative is written `+-1` ("Shrink
  both" in the viewer on a `+1` row). `get_params` then raises ValueError, TeX is given `+-1`, and
  on the next read `adjre` doesn't match so the row is dropped (tested). Only prefix `+` when
  `v >= 0`.
* `parlocs.py:644-645` (and `_getRectsPage` 581) `getParas` looks back only 2 entries before
  `pindex[pnum-1]` for a paragraph continuing from the previous page; in a diglot the other glot's
  continuing paragraph is often further back, so page-start keys (`page_memo`, `avoid_key`,
  `failed_starts`), `get_page_first_pid` and viewer click lookups get the wrong paragraph or none
  (tested, OGNT Diglot JAS: pages 5, 6, 9; p5 misses `JASR2.1[]`). Scan back until no earlier
  paragraph still has rects on the page, or index rects by page while reading.
* `page_filler.py:1183` the contrast term looks up `p` instead of `prev`, so `preve == pe` and
  `s_pbcontrast` has no effect (`prev` is computed and unused) (traced). Use
  `shape_cache.get((prev, combo.get(prev, 0)), self.neutral(prev))` when `prev` is not None.
* `page_filler.py:1422-1424, 1469` (used at 437-441) resume/restart in `PTXFiller`:
  `AdjList.get_params`/`get_cache` key rows `BK c.v[1]` but parlocs ids are `BK c.v[]` when TeX
  gave no parnum, so on a resume of a non-diglot book earlier adjustments are dropped, the
  shape cache never matches (no moves), and probing is off, so pages fail untried (tested:
  my_judson ROM 56/56 ids are `[]`). `PolySolver._match_adjlist_ids` (poly_filler.py:77-86)
  already fixes this for polyglots; apply it in `TypesetterSolver` too.
* `page_filler.py:1603-1610` with 437-441: on restart `createAdjs` starts from `init_adjs` (all
  old rows) and only `setval`s paragraphs in `parparms`, so rows the solver dropped from
  `base_params` keep their old stretch on disk; every run is measured against settings the solver
  thinks are neutral (traced, medium confidence). Reset rows not in `parparms` to neutral.
* `page_filler.py:664-670` vs 682: the page is judged full on a run with `probe_params`, and the
  straddler's probe shape is copied to `page_base_params`, but 682 commits
  `new_state.paragraph_params`, built without it; on the next page the straddler reverts, the page
  goes short and page+1 combos are rejected at 651. 665 also reads `state.layout` not
  `new_state` (traced, medium). Put the straddler's probe value into `new_state.paragraph_params`.
* `page_filler.py:619` vs 1064: `page_base_params[page]` is read before the `next_combination`
  generator overwrites it, so each visit uses the base saved on the previous visit; on a third
  repair visit `{B:+1}` is laid out as `{A:-1, B:+1}` while `tried_combos` (keyed by combo only)
  skips the clean one (traced, medium). Fix one base per visit, or key tried combos by base.
* `page_filler.py:1600, 1610, 1635`, `view.py:2058` percentages use `int(x*100)`:
  `int(1.15*100) == 114`, so max text limits 113-116% lose 1, and bisection midpoints truncate onto
  values already tried (1.01875 and 1.0125 both run at 101%) (tested). Use `round()`.

### GUI

* `gtkview.py:7971-8002` when Analyse & Fill finishes, `_pollFillProgress` reloads adjlists and
  calls `onOK` on whatever project/config is current *now*: the progress window is non-modal, so
  switching to project B mid-fill saves and prints B (resetting its adjlists/adjView) and A's PDF
  is never rebuilt (traced). Keep pid/guid/cfgid at start; on finish skip (or ask) if changed.
* `gtkview.py:4753-4756` unsaved picture-list edits are lost on switching project:
  `picListView.clear()`/`picinfos.clear()` run before `super().updateProjectSettings(saveCurrConfig=True)`
  saves, and `clear()` sets `loaded=False`, so both `savePics` skip writing (traced). Clear after
  the save, or `savePics()` first.
* `gtkview.py:5123-5139` auto-save / "Save changes?" on leaving a Viewer sub-tab saves the *new*
  tab: the focus-out handler computes `pgnum` from `widget.pageid` but calls `onSaveEdits(None)`,
  which uses `nbk_Viewer.get_current_page()` (3910), already switched; the edits are then lost on
  reload. Same in `onRefreshViewerTextClicked` (3598) (traced, medium: depends on GTK focus order).
  Pass `pgid=widget.pageid`.
* `gtkpolyglot.py:403-405` changing a row's project overwrites the first entry of the new
  config list with `new_cfg` instead of selecting it: Y's configs [Alpha, Default] show as
  [Default, Default] (traced). Delete those lines; 407 already sets the row's cfg.
* `gtkpolyglot.py:613-620, 678-692` (and `load_polyglots_into_treeview` 116-117) `ls_config` is
  indexed by row position but delete/move of a row never reorders it, so shifted rows offer
  another project's configs (traced). `pop`/`insert` the matching `ls_config` entry.
* `pdf_viewer.py:910` spread Next/Previous step by folio parity (`current_page` is a folio) but
  spreads are built from index parity (`get_spread` 1691-1703): after jumping to an even page, or
  when folio and index parity differ (front matter), a press lands on the same spread (traced,
  medium-high). Step ±2 from `get_spread(current_index)[0]`.
* `pdf_viewer.py:520-523` with 1293/1700-1701 RTL spreads are reversed twice (`get_spread` order
  and `pack_end`) in a fresh session, but once if the boxes were packed while viewing an LTR PDF
  (reused at 505), so RTL page order depends on what was previewed earlier (traced, medium).
  Reverse in one place; re-pack when `rtl_mode` changes.
* `view.py:1115-1160` `readConfig` sets `loadingConfig` with no `try/finally`; e.g. a project with
  no books raises IndexError at 1136 (`list(...)[0]`) and the flag stays True, silencing every
  handler that checks it (UI level, direction, grid, lock ratio...) until the next good load
  (traced, medium). `try/finally`, and guard the `[0]`.
* `gtkview.py:4836` vs 7580 the preview decides RTL from text direction (`self.rtl`) on project
  load but from `c_RTLbookBinding` after printing, so spread order and gutter guides change with
  RTL text + LTR binding (traced, medium). Use `c_RTLbookBinding` in both.
* `gtkpolyglot.py:139-146` `find_or_create_row` tests the 9-row limit before looking for an
  existing row, so with 9 rows every lookup (even "L") returns -1 and writes into the last row
  (traced, low-medium). Look up first; limit only when appending.

### Config and model

* `view.py:1132` with 1596-1598 `readConfig` runs `versionFwdConfig` on `ptxprint_override.cfg`
  and `ptxprint_project.cfg`, which always sets `project/colophontext` (to "" if absent); the
  locked override then blanks the colophon and the next save writes `colophontext =` (tested,
  WSGlatin with a one-line project cfg). Only apply such fix-ups when the option is present, or
  don't version-forward override files.
* `view.py:1788-1795` the `_settingmappings` loop also runs for override loads (`clearvars=False`):
  `fncallers`/`xrcallers` missing from the override are reset to Paratext's (`*`), and
  `createConfig:1253` then drops them because they equal ptsettings — custom callers lost for good
  (tested). Only run the loop when `clearvars`.
* `view.py:1733-1746` with 1231-1242 `_attributes` paths (FrontPDFs, BackPDFs, watermarks,
  pageborder, sectionheader, endofbook, customScript, customXRfile, coverImage, ...) are never reset
  on a config switch: config B prints with A's border/watermark/script and saving writes A's paths
  into B (tested: DecorRUT → MinimalOdd). Reset every `_attributes` value at the start of a
  clearvars load.
* `view.py:1118, 1137-1157` with 1272-1274 `self.polyglots` is only rebuilt from `diglot_*`
  sections when `c_diglot` is on, and `createConfig` writes only what is in it: untick diglot,
  reload, save, and `[diglot_L]`/`[diglot_R]` are deleted (tested, Diglot2JN). Always read the
  sections; only create the views when diglot is on.
* `snippets.py:251` the diglot secondary's hyphenation is `\input` from `{diglot[/cfgrpath]}`
  (the config folder), but the file is in `shared/ptxprint/` (`hyphen.py:16`, `template.tex:271`),
  where `texmodel.py:252` found it to set `ifhavehyphenate`: XeTeX fails on a missing file
  (traced). Use the same path as the template.
* `view.py:818-824, 858-862` "Copy config to other projects → Merge" opens `destp` and
  `<newp>/base/...` unconditionally; a target config not made by an earlier copy (no `base/`), or
  lacking a file the source has (changes.txt, FRTlocal.sfm), raises FileNotFoundError and the
  remaining files are skipped, leaving it half-merged (traced). Plain copy when `destp` is
  missing; treat a missing base as empty.
* `utils.py:943`, 913-928 `withvars` stores `os.path.relpath` (backslashes on Windows) after a
  `/`, and `Path` never converts `\` back on POSIX: `${pdfassets}/border-art\A5 page border.pdf`
  is not found on Linux (traced; 13 WSGlatin test configs contain such paths, medium-high).
  Normalise `\` to `/` in both places.
* `view.py:1128` override/project cfgs are read as `utf-8`, not `utf-8-sig` like the main cfg
  (1107): a Notepad-saved file with a BOM raises MissingSectionHeaderError and no overrides apply
  (tested). Use `utf-8-sig` (also `_readLangVars`, `_writeLangVars`, `_mergecfg`).
* Minor: v<1.502 upgrade tests `includimg` (typo); `view.py:1403` `bits += [] * n` is a no-op;
  `texmodel.py:614` `210 / unitConv["mm"]` should be `*` (practically unreachable).

### Print job and PDF post-processing

* `pdf/procpdf.py:56-66` with a cover and "extract inserts" off, `split_pages` still removes every
  tagged insert but only writes the cover back: map pages (`\PullPeriph{maps}` is the default)
  vanish from the final PDF (tested: 4 pages → 2). Split out only the cover when burst is off.
* `pdf/pdfimage.py:176` `bytes(x)` on an int gives x zero bytes: Spot-output images get a stream
  of zeros of the wrong length (tested: 4 pixels → 1221 bytes). Build the stream from the byte
  values (`bytes(z)`) or interleave with numpy.
* `pdf/fixcol.py:257`, `pdf/pdfimage.py:207,217` spot maths: text/drawing tint is
  `spothsv[1]/hsv[1]` (inverted; pale red gives 5.00); image `spotb = v - maxv` is never positive
  and wraps in uint8 (darker pixels get heavy black); `np.isclose(hue, h, hrange)` passes rtol not
  atol (tested). Invert the ratio, use `maxv - v` clipped, `atol=hrange`.
* `pdf/fixcol.py:173-176, 191` CMYK conversion: the grey test applies 0.05 to a sum of squares
  (~0.16 per channel) and takes the level from `r`, so pale pink → white, light blue → grey
  (tested, medium-high that it's unintended); `vals >= self.threshold` compares a list with a float,
  the TypeError is swallowed, so black overprint never happens (tested). Per-channel tolerance
  ~0.01 with luminance; test `max(vals[:3])`/`vals[3]`.
* `runjob.py:183` (`doit`/`dojob`/`sharedjob`) `lockme` has no try/finally; after an exception in a
  reused worker process (or `-j 1`) every later job returns False at once with no message
  (traced). Unlock in a finally, or in `execute_job`'s except.
* `multiprint.py:426` `" ".join(job.books)` on a RefList → TypeError when a publication job
  raised: the summary is lost (tested). Use `str(job.books)`.
* `publications.py:309`, `multiprint.py:236, 71` module publications can't print: the GUI submits
  `[books]` (a list), `execute_job` calls `job.books.first` outside its try, and `ViewPrinter.solve`
  sets `self.moduleFile` not `self.view.moduleFile`; `_pollProgress` (publications.py:352) never
  reads `get_results`, so all failures look like success (traced).
* `gtkview.py:7911-7917` starting Analyse & Fill `terminate()`s the shared `self.mprint`, killing
  publications being printed; the reverse also mixes the two pools (traced). Separate
  MultiPrints, or refuse while busy.
* `runjob.py:733` with 816-824 the rerun check compares XeTeX's raw `.toc` with the one Python
  rewrote last time, so every print with a TOC does an extra XeTeX run (Quick Run always says
  "Rerun to fix: table of contents") (traced). Compare with the `_org` copy.
* `pdf/procpdf.py:144-174` scale to fit scales MediaBox and content but not TrimBox (every page
  has one, `ptx-cropmarks.tex:421-426`), nor MediaBox origin offsets: TrimBox ends up in a corner,
  or larger than the MediaBox (invalid PDF/X) (traced, medium-high). Transform Trim/Bleed/ArtBox too.
* `view.py:1308-1607`, `texmodel.py:254-260` `--readonly` still writes shared files through
  `versionFwdConfig` (blank ptxprint.sty when missing, changes.txt rewrite, .adj deletion,
  piclist renames, ...) and TexModel's PrintDraft-mods.sty copy; the diglot side ViewModel
  (`view.py:2354`) is made without args, so it's never read-only (traced). Skip file side effects
  when `readOnly`; pass `args`.
* `pdf/procpdf.py:136-140` an imposition OverflowError returns `{}` not `None`, so the CLI exits 0
  with the un-imposed PDF (traced). Return `None`.

### Text, pictures, styles, fonts

* `changes.py:89` nested contexts: `domatch` passes `lambda x: fn(m.group(0))`, applying the
  change to the outer match and putting that in place of the inner match, so any rule with two
  scopes (`at GEN 1:2 in "\f .*?\f\*": ...`, or two `in` clauses) duplicates text (tested). Use
  `lambda x: fn(x)`.
* `usxutils.py:161-182` `mrktype`: `set(sheet.get('occursunder'))` is a set of characters, and
  lower-cased TextType/StyleType are compared with mixed-case `'NoteText'`, `'VerseText'`,
  `'Standalone'`; a custom note marker (`\StyleType Note`, `\TextType NoteText`) becomes `char`, so
  `\zfn + \ft note\zfn*` text spills into the verse; custom standalone markers get no category
  (tested). Split OccursUnder into words, compare case-insensitively, map Note to footnote.
* `usfmerge.py:222/713/490` subverses: `3a`/`3b` reduce to the same `position`; `score()` keeps
  only the last index in `self.loc[pos]`, so L's 3a sits opposite R's v2 (tested, both score
  modes). Include the subverse letter, or keep the first index on collision.
* `usfmerge.py:655` `elif c.type in (CHAPTER, BODY, PREVERSEPAR)` tests `c` (always HEADING there)
  instead of `cn`, so every heading not followed by a verse-start paragraph becomes INTRO; the
  "heading before \c" merge (662) is dead, and L's `\s` before `\c 2` prints at the foot of chapter
  1 while R's goes with `\c 2` (tested; intended outcome per case: medium).
* `usfmerge.py:423-429` a mid-verse paragraph that also starts the next verse
  (`\q2 rest of v1. \v 2 ...`) is labelled PREVERSEPAR because `c.text` is never checked, so v1's
  second line goes in the v2 row and v2/v3 collapse (tested). Use `midvmode` when the paragraph
  has leading text.
* `font.py:1329` `updateTeXStyle` writes `FontName = self.name`, dropping the face from
  `_getTeXComponents` (Semibold, Light...), so "Segoe UI Semibold" prints as regular; and 1316's
  `_iseq(ignorestyle=True)` drops FontName when the family matches the body font (tested; how
  often the UI produces such a FontRef: medium). Use `name`.
* `font.py:658-707` `TTFont.cache` keeps "not found" entries (filename None) all session;
  `addFontDir`/`runFcCache` never clear it, so a font installed later, or shipped in another
  project's `shared/fonts`, stays missing and a Graphite font loses `/GR` until restart; the first
  project's same-named font wins for later projects (tested). Don't cache misses; clear on
  font-dir changes.
* Lower impact (traced): `usfmerge.py:897` `chlist=('CHAPTERHEAD')` is a string, so `'CHAPTER' in
  chlist` is true by substring (`\c N` always alone in its row); 901 tests `positions[...][3]` not
  `[_headingidx]`, so heading back-up never runs; 817/857 broken but unreachable align modes;
  `piclist.py:761` `['anchor'][3:4]` is always `[]` (sort order only).

### TeX macros

* `ptx-figure.tex:962` `\uppercase{\def\t@mp{\l@cspec@b}}` only uppercases the letters it sees, so
  `\t@mp` is `macro:->\l@cspec@b` and `\ifx\t@mp\m@x@at@col` is never true: in a diglot a top
  picture's own column is never recognised as the tallest, so a second `tL` picture smaller than
  the first counts 0pt against `\pagegoal` (1204-1208) and too much text is let in (ran the
  construct; layout effect traced, medium-high). `\edef` first, then `\uppercase` via `\x@`.
* `ptx-output.tex:1112, 1083` "Enhanced paragraphed footnotes" shaving: 1112 records
  `\ht\n@tesbox - \sh@vedim`, but `\findsh@venotes` runs inside `\m@kenotebox`, while `\n@tesbox`
  still holds the previous trial's/page's box of all classes; should be `\ht\@sh@venotebox`. 1083
  tests scratch `\ht0` instead of `\ht#1`. Shaving is skipped or moves the wrong amount (negative
  on the first page with notes) (traced, high).
* `ptx-figure.tex:849-850` `\lowercase{\edef\size@ption{\csname figparam-size\endcsname}}`
  lowercases the name, not the value: `size="Span"` stops with `Unknown picture size` (920)
  (ran it; not checked whether Python lowercases first). Same pattern at `ptx-extended.tex:628`
  (`FigScaleTo`). `\edef` first, then `\lowercase` via `\x@`.
* `ptx-para-style.tex:434` the `\@parend` record's `{\the\lastdepth}` stays inside the deferred
  `\write`, so it is the value at shipout (often 0pt after a title gridbox, 262), and the write
  precedes `\p@r` anyway; `parlocs.py:409` subtracts it from `yend`, so paragraph ends the filler
  uses are off by a descender (traced, medium-high; impact low-medium). Write after `\p@r` with
  the depth expanded at once.
* `ptx-adj-list.tex:169` `\ifadjslurp\else ... \else ... \fi\fi` has two `\else`: with
  `\adjslurpfalse` and trace `j`, every `\ch@ckadjustments` gives `! Extra \else.` (ran it; debug
  path only).
* Minor: `ptx-adj-list.tex:66` `\warnspace #1 \E` passes the book code, not `#3`, so the
  "no spaces in adjustlist entries" warning never fires; `ptx-output.tex:474, 1512`
  `\multiply\dimen5 by 32` overflows when the column-notes xref box is >512pt taller than the
  column (guard at 445 only stops at 2000pt) (traced, unlikely).
