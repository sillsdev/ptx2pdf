import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .sectionBase import (SectionPanel, makeVBox, makeHBox, makeCheck,
                           makeCombo, makeFrame, makeSectionTitle, makeButton)

logger = logging.getLogger(__name__)

SCOPE_OPTIONS = [
    ("wholeBible",   "Whole Bible"),
    ("newTestament", "New Testament"),
    ("oldTestament", "Old Testament"),
    ("portion",      "Scripture portion (selected books)"),
    ("custom",       "Custom selection"),
]

# USFM book codes — OT then NT
OT_BOOKS = [
    ("GEN","Genesis"),("EXO","Exodus"),("LEV","Leviticus"),("NUM","Numbers"),
    ("DEU","Deuteronomy"),("JOS","Joshua"),("JDG","Judges"),("RUT","Ruth"),
    ("1SA","1 Samuel"),("2SA","2 Samuel"),("1KI","1 Kings"),("2KI","2 Kings"),
    ("1CH","1 Chronicles"),("2CH","2 Chronicles"),("EZR","Ezra"),("NEH","Nehemiah"),
    ("EST","Esther"),("JOB","Job"),("PSA","Psalms"),("PRO","Proverbs"),
    ("ECC","Ecclesiastes"),("SNG","Song of Songs"),("ISA","Isaiah"),("JER","Jeremiah"),
    ("LAM","Lamentations"),("EZK","Ezekiel"),("DAN","Daniel"),("HOS","Hosea"),
    ("JOL","Joel"),("AMO","Amos"),("OBA","Obadiah"),("JON","Jonah"),
    ("MIC","Micah"),("NAM","Nahum"),("HAB","Habakkuk"),("ZEP","Zephaniah"),
    ("HAG","Haggai"),("ZEC","Zechariah"),("MAL","Malachi"),
]
NT_BOOKS = [
    ("MAT","Matthew"),("MRK","Mark"),("LUK","Luke"),("JHN","John"),
    ("ACT","Acts"),("ROM","Romans"),("1CO","1 Corinthians"),("2CO","2 Corinthians"),
    ("GAL","Galatians"),("EPH","Ephesians"),("PHP","Philippians"),("COL","Colossians"),
    ("1TH","1 Thessalonians"),("2TH","2 Thessalonians"),("1TI","1 Timothy"),
    ("2TI","2 Timothy"),("TIT","Titus"),("PHM","Philemon"),("HEB","Hebrews"),
    ("JAS","James"),("1PE","1 Peter"),("2PE","2 Peter"),("1JN","1 John"),
    ("2JN","2 John"),("3JN","3 John"),("JUD","Jude"),("REV","Revelation"),
]
ALL_BOOKS = OT_BOOKS + NT_BOOKS


class ContentSection(SectionPanel):
    sectionId = "content"

    def _buildUi(self):
        self.pack_start(makeSectionTitle("What Scripture content to include?"), False, False, 0)

        # Scope radio group
        scopeFrame = makeFrame("Scripture scope")
        scopeInner = makeVBox(spacing=4)
        scopeInner.set_margin_start(8)
        scopeInner.set_margin_end(8)
        scopeInner.set_margin_top(6)
        scopeInner.set_margin_bottom(6)

        self._scopeRadios = {}
        group = None
        for scopeId, scopeLabel in SCOPE_OPTIONS:
            radio = Gtk.RadioButton.new_with_label_from_widget(group, scopeLabel)
            radio.show()
            if group is None:
                group = radio
            radio.connect("toggled", self._onScopeToggled, scopeId)
            scopeInner.pack_start(radio, False, False, 0)
            self._scopeRadios[scopeId] = radio

        scopeInner.show()
        scopeFrame.add(scopeInner)
        scopeFrame.show()
        self.pack_start(scopeFrame, False, False, 0)

        # Book list filter + bulk actions
        filterRow = makeHBox(spacing=8)
        self._filterReadyCheck = Gtk.CheckButton(label="Show ready books only")
        self._filterReadyCheck.connect("toggled", self._onFilterToggled)
        self._filterReadyCheck.show()

        btnSelectReady = makeButton("Select all ready")
        btnSelectReady.connect("clicked", lambda _b: self._selectScope("ready"))
        btnSelectNT = makeButton("Select NT")
        btnSelectNT.connect("clicked", lambda _b: self._selectScope("nt"))
        btnSelectOT = makeButton("Select OT")
        btnSelectOT.connect("clicked", lambda _b: self._selectScope("ot"))

        filterRow.pack_start(self._filterReadyCheck, False, False, 0)
        filterRow.pack_end(btnSelectOT, False, False, 0)
        filterRow.pack_end(btnSelectNT, False, False, 0)
        filterRow.pack_end(btnSelectReady, False, False, 0)
        filterRow.show()
        self.pack_start(filterRow, False, False, 0)

        # Book list (scrolled)
        self._bookChecks = {}
        self._bookStatus = {}  # usfm -> "ready"|"inProgress"|"notStarted"|"hasErrors"

        bookListBox = makeVBox(spacing=2)
        for usfm, bookName in ALL_BOOKS:
            row = makeHBox(spacing=6)
            chk = Gtk.CheckButton(label=f"{usfm}  {bookName}")
            chk.show()
            chk.connect("toggled", self._onBookToggled)
            statusLbl = Gtk.Label(label="⚪")
            statusLbl.show()
            row.pack_start(chk, True, True, 0)
            row.pack_start(statusLbl, False, False, 0)
            row.show()
            bookListBox.pack_start(row, False, False, 0)
            self._bookChecks[usfm] = chk
            # store status label for later update from PTXprint integration
            self._bookStatus[usfm] = statusLbl

        bookListBox.show()

        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.set_min_content_height(200)
        sw.add(bookListBox)
        sw.show()
        self.pack_start(sw, True, True, 0)

        # Include unchecked
        self._includeUncheckedCheck = Gtk.CheckButton(
            label="Include books that have not passed all Paratext checks (shows warning)")
        self._includeUncheckedCheck.connect("toggled", self._onChange)
        self._includeUncheckedCheck.show()
        self.pack_start(self._includeUncheckedCheck, False, False, 0)

        # Diglot / triglot
        multiRow = makeHBox(spacing=16)
        self._diglotCheck = Gtk.CheckButton(label="Diglot (two parallel languages)")
        self._diglotCheck.connect("toggled", self._onDiglotToggled)
        self._diglotCheck.show()

        self._triglotCheck = Gtk.CheckButton(label="Triglot (three parallel languages)")
        self._triglotCheck.connect("toggled", self._onTriglotToggled)
        self._triglotCheck.show()

        multiRow.pack_start(self._diglotCheck, False, False, 0)
        multiRow.pack_start(self._triglotCheck, False, False, 0)
        multiRow.show()
        self.pack_start(multiRow, False, False, 0)

        # Secondary / tertiary project pickers (hidden unless diglot/triglot)
        self._secondaryBox = makeHBox(spacing=8)
        secLbl = Gtk.Label(label="Secondary project:")
        secLbl.show()
        self._secondaryEntry = Gtk.Entry()
        self._secondaryEntry.set_placeholder_text("Project name or path")
        self._secondaryEntry.set_hexpand(True)
        self._secondaryEntry.connect("changed", self._onChange)
        self._secondaryEntry.show()
        self._secondaryBox.pack_start(secLbl, False, False, 0)
        self._secondaryBox.pack_start(self._secondaryEntry, True, True, 0)
        self._secondaryBox.show()
        self._secondaryBox.set_no_show_all(True)
        self._secondaryBox.set_visible(False)
        self.pack_start(self._secondaryBox, False, False, 0)

        self._tertiaryBox = makeHBox(spacing=8)
        terLbl = Gtk.Label(label="Tertiary project:")
        terLbl.show()
        self._tertiaryEntry = Gtk.Entry()
        self._tertiaryEntry.set_placeholder_text("Project name or path")
        self._tertiaryEntry.set_hexpand(True)
        self._tertiaryEntry.connect("changed", self._onChange)
        self._tertiaryEntry.show()
        self._tertiaryBox.pack_start(terLbl, False, False, 0)
        self._tertiaryBox.pack_start(self._tertiaryEntry, True, True, 0)
        self._tertiaryBox.show()
        self._tertiaryBox.set_no_show_all(True)
        self._tertiaryBox.set_visible(False)
        self.pack_start(self._tertiaryBox, False, False, 0)

    def _onScopeToggled(self, radio, scopeId):
        if not self._loading and radio.get_active():
            self._applyScopeToChecks(scopeId)
            self._emitStateChanged()

    def _applyScopeToChecks(self, scopeId):
        otCodes = {b[0] for b in OT_BOOKS}
        ntCodes = {b[0] for b in NT_BOOKS}
        if scopeId == "wholeBible":
            for chk in self._bookChecks.values():
                chk.set_active(True)
        elif scopeId == "newTestament":
            for code, chk in self._bookChecks.items():
                chk.set_active(code in ntCodes)
        elif scopeId == "oldTestament":
            for code, chk in self._bookChecks.items():
                chk.set_active(code in otCodes)
        # portion/custom: leave checks as-is

    def _onBookToggled(self, *_args):
        self._emitStateChanged()

    def _onFilterToggled(self, *_args):
        showReady = self._filterReadyCheck.get_active()
        # TODO(integrate): filter based on real check status from PTXprint
        pass

    def _onChange(self, *_args):
        self._emitStateChanged()

    def _onDiglotToggled(self, chk):
        active = chk.get_active()
        self._secondaryBox.set_visible(active)
        if not active:
            self._triglotCheck.set_active(False)
        self._emitStateChanged()

    def _onTriglotToggled(self, chk):
        active = chk.get_active()
        self._tertiaryBox.set_visible(active)
        if active:
            self._diglotCheck.set_active(True)
        self._emitStateChanged()

    def _selectScope(self, scope):
        otCodes = {b[0] for b in OT_BOOKS}
        ntCodes = {b[0] for b in NT_BOOKS}
        for code, chk in self._bookChecks.items():
            if scope == "nt":
                chk.set_active(code in ntCodes)
            elif scope == "ot":
                chk.set_active(code in otCodes)
            elif scope == "ready":
                # TODO(integrate): check real status from PTXprint
                pass
        self._emitStateChanged()

    def updateBookStatuses(self, statuses):
        """Update status icons from PTXprint. statuses: {usfmCode: 'ready'|'inProgress'|'notStarted'|'hasErrors'}"""
        ICONS = {"ready": "✅", "inProgress": "🟡", "notStarted": "⚪", "hasErrors": "⚠"}
        for code, statusLbl in self._bookStatus.items():
            status = statuses.get(code, "notStarted")
            statusLbl.set_text(ICONS.get(status, "⚪"))

    def _getSelectedBooks(self):
        return [code for code, chk in self._bookChecks.items() if chk.get_active()]

    def _getActiveScope(self):
        for scopeId, radio in self._scopeRadios.items():
            if radio.get_active():
                return scopeId
        return None

    def loadFromState(self, state):
        self._loading = True
        scope = state.content.scope
        if scope and scope in self._scopeRadios:
            self._scopeRadios[scope].set_active(True)

        selected = set(state.content.selectedBooks)
        for code, chk in self._bookChecks.items():
            chk.set_active(code in selected)

        self._includeUncheckedCheck.set_active(state.content.includeUnchecked)
        self._diglotCheck.set_active(state.content.isDiglot)
        self._triglotCheck.set_active(state.content.isTriglot)
        self._secondaryBox.set_visible(state.content.isDiglot)
        self._tertiaryBox.set_visible(state.content.isTriglot)
        if state.content.secondaryProject:
            self._secondaryEntry.set_text(state.content.secondaryProject)
        if state.content.tertiaryProject:
            self._tertiaryEntry.set_text(state.content.tertiaryProject)
        self._loading = False

    def saveToState(self, state):
        state.content.scope = self._getActiveScope()
        state.content.selectedBooks = self._getSelectedBooks()
        state.content.includeUnchecked = self._includeUncheckedCheck.get_active()
        state.content.isDiglot = self._diglotCheck.get_active()
        state.content.isTriglot = self._triglotCheck.get_active()
        state.content.secondaryProject = self._secondaryEntry.get_text() or None
        state.content.tertiaryProject = self._tertiaryEntry.get_text() or None

    def isComplete(self):
        scope = self._getActiveScope()
        if scope is None:
            return False
        if scope in ("portion", "custom"):
            return bool(self._getSelectedBooks())
        return True
