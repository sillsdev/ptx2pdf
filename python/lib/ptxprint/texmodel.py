import configparser, re, os, traceback, sys
from shutil import copyfile
from functools import reduce
from inspect import signature
import regex
from ptxprint.font import TTFont
from ptxprint.runner import checkoutput
from ptxprint.usxutils import Usfm, Sheets
from ptxprint.module import Module
from ptxprint.utils import _, universalopen, localhdrmappings, pluralstr, multstr, \
                            chaps, books, bookcodes, allbooks, oneChbooks, f2s, cachedData, pycodedir, \
                            runChanges, booknumbers, Path, nonScriptureBooks, saferelpath, texprotect
from ptxprint.dimension import Dimension
import ptxprint.scriptsnippets as scriptsnippets
from ptxprint.interlinear import Interlinear
from ptxprint.reference import Reference, RefRange, RefList, RefSeparators, AnyBooks
from ptxprint.xrefs import Xrefs
from ptxprint.pdf.pdfsanitise import sanitise
from ptxprint.texpert import TeXpert
from ptxprint.modelmap import ModelMap
from usfmtc.versification import Versification
import ptxprint.modelmap as modelmap
import logging

logger = logging.getLogger(__name__)

# After universalopen to resolve circular import. Kludge
from ptxprint.snippets import FancyIntro, PDFx1aOutput, Diglot, FancyBorders, ThumbTabs, Colophon, Grid, ParaLabelling

def loosint(x):
    try:
        return int(x)
    except (ValueError, TypeError):
        return 0

def makeChange(pattern, to, flags=regex.M, context=None):
    frame =  traceback.extract_stack(limit=2)[0]
    # print(f"'{pattern}' > '{to}' # {flags}")
    return (context, regex.compile(pattern, flags), to, f"{frame.filename} line {frame.lineno}")
    
bcvref = re.compile(r'([A-Z]{3})\s*(\d+)[.:](\d+(?:-\d+)?)')

Borders = {'c_inclPageBorder':      ('pageborder', 'fancy/pageborderpdf', 'A5 page border.pdf'),
           'c_inclSectionHeader':   ('sectionheader', 'fancy/sectionheaderpdf', 'A5 section head border.pdf'),
           'c_inclEndOfBook':       ('endofbook', 'fancy/endofbookpdf', 'decoration.pdf'),
           'c_inclVerseDecorator':  ('versedecorator', 'fancy/versedecoratorpdf', 'Verse number star.pdf'),
           'c_inclFrontMatter':     ('FrontPDFs', 'project/frontincludes', '\\includepdf{{{}}}'),
           'c_inclBackMatter':      ('BackPDFs', 'project/backincludes', '\\includepdf{{{}}}'),
           'c_applyWatermark':      ('watermarks', 'paper/watermarkpdf', r'\def\MergePDF{{"{}"}}')
}

_periphids = {
    "title page": "title",
    "half title page": "halftitle",
    "promotional page": "promo",
    "imprimatur": "imprimatur",
    "publication data": "pubdata",
    "foreword": "foreword",
    "preface": "preface",
    "table of contents": "contents",
    "alphabetical contents": "alphacontents",
    "table of abbreviations": "abbreviations",
    "bible introduction": "intbible",
    "old testament introduction": "intot",
    "pentateuch introduction": "intpent",
    "history introduction": "inthistory",
    "poetry introduction": "intpoetry",
    "prophecy introduction": "intprophesy",
    "deuterocanon introduction": "intdc",
    "new testament introduction": "intnt",
    "gospels introduction": "intgospels",
    "epistles introduction": "intepistles",
    "letters introduction": "intletters",
    "chronology": "chron",
    "weights and measures": "measures",
    "map index": "maps",
    "lxx quotes in nt": "lxxquotes",
    # "coverfront": "coverfront",
    # "coverback": "coverback",
    # "coverspine": "coverspine",
    # "coverwhole": "coverwhole",
    "cover": "cover",
    "spine": "spine"
}


class TexModel:
    _ptxversion = 4
    _peripheralBooks = ["FRT", "INT"]
    _bookinserts = (("GEN-REV", "intbible"), ("GEN-MAL", "intot"), ("GEN-DEU", "intpent"), ("JOS-EST", "inthistory"),
                    ("JOB-SNG", "intpoetry"), ("ISA-MAL", "intprophecy"), ("TOB-LAO", "intdc"), 
                    ("MAT-REV", "intnt"), ("MAT-JHN", "intgospels"), ("ROM-PHM", "intepistles"), ("HEB-REV", "intletters"))
    _fonts = {
        "fontregular":              ("bl_fontR", None, None, None, None),
        "fontbold":                 ("bl_fontB", None, "c_fakebold", "fontbold/embolden", "fontbold/slant"),
        "fontitalic":               ("bl_fontI", None, "c_fakeitalic", "fontitalic/embolden", "fontitalic/slant"),
        "fontbolditalic":           ("bl_fontBI", None, "c_fakebolditalic", "fontbolditalic/embolden", "fontbolditalic/slant"),
        "fontextraregular":         ("bl_fontExtraR", "c_useFallbackFont", None, None, None),
    }
    _mirrorRL = {r'\lastref':    r'\firstref',
                 r'\firstref':   r'\lastref'
    }
    _swapRL = {'left':   'right',
               'center': 'center',
               'right':  'left'
    }
    _glossarymarkup = {
        "ai": r"\1",                # "As is (pass|through)":
        "no": r"\1",                # "None":
        None: r"\1",                # None:
        "bd": r"\\+bd \1\\+bd*",      # "format as bold":
        "it": r"\\+it \1\\+it*",      # "format as italics":
        "bi": r"\\+bdit \1\\+bdit*",  # "format as bold italics":
        "em": r"\\+em \1\\+em*",      # "format with emphasis":
        "ww":  r"\\+w \1\\+w*",       # "\w ...\w* char style":
        # Note that these glossary markers can be styled with \zglm 
        # But this doesn't work if fallback font is turned on for these chars
        "fb": r"\\+zglm \u2E24\\+zglm*\1\\+zglm \u2E25\\+zglm*",    # "with ⸤floor⸥ brackets":   
        "fc": r"\\+zglm \u230a\\+zglm*\1\\+zglm \u230b\\+zglm*",    # "with ⌊floor⌋ characters": 
        "cc": r"\\+zglm \u231e\\+zglm*\1\\+zglm \u231f\\+zglm*",    # "with ⌞corner⌟ characters":
        "sb": r"*\1",               # "star *before word":       
        "sa": r"\1*",               # "star after* word":        
        "cb": r"^\1",               # "circumflex ^before word": 
        "ca":  r"\1^"               # "circumflex after^ word":  
    }
    _snippets = {
        "snippets/fancyintro":            ("c_prettyIntroOutline", None, FancyIntro),
        "snippets/pdfoutput":             ("fcb_outputFormat", lambda x: True, PDFx1aOutput),
        "snippets/diglot":                ("c_diglot", None, Diglot),
        "snippets/fancyborders":          ("c_useOrnaments", None, FancyBorders),
        "snippets/thumbtabs":             ("c_thumbtabs", None, ThumbTabs),
        "snippets/colophon":              ("c_colophon", None, Colophon),
        "snippets/grid":                  ("c_gridLines", None, Grid),
        "texpert/showusfmcodes":          ("c_showusfmcodes", None, ParaLabelling)
    }
    _settingmappings = {
        "notes/xrcallers": "crossrefs",
        "notes/fncallers": "footnotes"
    }
    _crossRefInfo = None

    _tocleaders = [
        "",
        r"\hskip .5pt .\hskip .5pt",
        r"\hskip 3pt .\hskip 3pt",
        r"\hskip 6pt \emdash\hskip 3pt",
        r"\hrule"
    ]

    _specialchars = {
        '*': 'asterisk',
        '%': 'percent',
        '#': 'hash',
        '$': 'dollar',
        '&': 'ampersand',
        '^': 'circumflex'
    }
        # '|': 'pipe'

    def __init__(self, printer, ptsettings, prjid=None, inArchive=False, diglotbinfo=None, digcfg=None):
        from ptxprint.view import VersionStr, GitVersionStr
        self.VersionStr = VersionStr
        self.GitVersionStr = GitVersionStr
        self.printer = printer
        self.ptsettings = ptsettings
        self.inArchive = inArchive
        self.changes = {}
        self.localChanges = None
        self.debug = False
        self.interlinear = None
        self.imageCopyrightLangs = {}
        self.found_glosses = None
        self.frontperiphs = None
        self.xrefs = None
        self.inserts = {}
        self.usedfiles = {}
        self.tablespans = set()
        libpath = pycodedir()
        path = printer.project.path
        printpath = printer.project.printPath(printer.cfgid)
        self.dict = {"/ptxpath": str(path).replace("\\","/"),
                     "/ptxprintlibpath": libpath.replace("\\","/"),
                     "/iccfpath": os.path.join(libpath, "default_cmyk.icc").replace("\\","/"),
                     "/ptx2pdf": self.printer.scriptsdir.replace("\\", "/"),
                     "/ptxdocpath": printpath.replace("\\", "/")}
        self.prjid = prjid
        if self.prjid is not None:
            self.dict['project/id'] = self.prjid
        self._hdrmappings = localhdrmappings()
        if self.printer is not None:
            # self.sheets = Sheets(self.printer.getStyleSheets(generated=True))
            self.update(diglotbinfo, digcfg=digcfg)

    def docdir(self, base=None):
        #base = os.path.join(self.dict["/ptxpath"], self.dict["project/id"])
        if base is None:
            base = self
        basedir = base.dict["/ptxpath"]
        docdir = base.dict["/ptxdocpath"]
        logger.debug(f"TeX model basepaths: {basedir=}, {docdir=}")
        return docdir, basedir

    def update(self, diglotbinfo, digcfg=None):
        """ Update model from UI """
        j = os.path.join
        rel = lambda x, y:saferelpath(x, y).replace("\\", "/")
        self.printer.setDate()  # Update date/time to now
        cpath = self.printer.project.srcPath(self.printer.cfgid)
        self.updatefields(ModelMap.keys())
        self.dict['project/id'] = self.printer.project.prjid
        docdir, base = self.docdir(base=diglotbinfo)
        self.dict["document/directory"] = "." # os.path.abspath(docdir).replace("\\","/")
        self.dict['project/adjlists'] = rel(j(cpath, "AdjLists"), docdir).replace("\\","/") + "/"
        self.dict['project/triggers'] = rel(j(cpath, "triggers"), docdir).replace("\\","/") + "/"
        self.dict['project/piclists'] = rel(j(self.printer.project.printPath(self.printer.cfgid), "tmpPicLists"), docdir).replace("\\","/") + "/"
        self.dict['config/name'] = self.printer.cfgid
        self.dict['/ptxrpath'] = rel(self.dict['/ptxpath'], docdir)
        self.dict['/cfgrpath'] = rel(cpath, docdir)
        self.dict['/ptxprint_version'] = self.VersionStr
        self.dict['/ptxprint_gitversion'] = self.GitVersionStr
        self.processHdrFtr(self.printer)
        # sort out caseless figures folder. This is a hack
        for p in ("Figures", "figures"):
            picdir = j(base, p)
            if os.path.exists(picdir):
                break
        self.dict["project/picdir"] = rel(picdir, docdir).replace("\\","/")
        # Look in local Config folder for ptxprint-mods.tex, and drop back to shared/ptxprint if not found
        fpath = j(cpath, "ptxprint-mods.tex")
        self.dict['/modspath'] = rel(fpath, docdir).replace("\\","/")
        fpath = j(cpath, "ptxprint-premods.tex")
        self.dict['/premodspath'] = rel(fpath, docdir).replace("\\","/")
        if digcfg is not None:
            digcfg.updateTM(self)
        if "document/diglotcfgrpath" not in self.dict:
            self.dict["document/diglotcfgrpath"] = ""
        self.dict['paragraph/linespacingfactor'] = f2s(float(self.dict['paragraph/linespacing']) \
                    / float(self.dict["texpert/linespacebase"]) / float(self.dict['paper/fontfactor']), dp=8)
        self.dict['paragraph/ifhavehyphenate'] = "" if os.path.exists(os.path.join(self.printer.project.srcPath(None), \
                                                       "hyphen-"+self.dict["project/id"]+".tex")) else "%"
        # forward cleanup. If ask for ptxprint-mods.tex but don't have it, copy PrintDraft-mods.tex
        if self.dict["project/ifusemodssty"] == "":
            modspath = os.path.join(cpath, "ptxprint-mods.sty")
            if not os.path.exists(modspath):
                spath = os.path.join(docdir, "PrintDraft-mods.sty")
                if os.path.exists(spath):
                    copyfile(spath, modspath)
        self.dict["paper/pagegutter"] = "{:.2f}mm".format(Dimension(self.dict["paper/width"]).asunits("mm") \
                        - (self.dict["paper/gutter"] if self.dict["paper/ifaddgutter"] == "true" else 0.))
        if self.dict["project/interlinear"] != "%":
            self.interlinear = Interlinear(self.dict["project/interlang"], self.dict["/ptxpath"])
        regfont = self.printer.get("bl_fontR")
        if regfont is not None:
            if regfont.isCtxtSpace:
                spcnt = 2
                self.dict["document/ifletter"] = "%"
                self.dict["document/letterspace"] = 0
                #self.dict["document/ifspacing"] = "%"
            else:
                spcnt = 0
            self.dict["document/spacecntxtlztn"] = str(spcnt)
            self.calculateMargins()
        if self.inArchive:
            for b, a in Borders.items():
                if self.dict[a[1]] is None or not self.dict[a[1]]:
                    continue
                islist = a[2].startswith("\\")
                fname = getattr(self.printer, a[0], (None if islist else a[2]))
                if fname is None:
                    fname = Path("." if islist else a[2])
                if islist and not isinstance(fname, (list, tuple)):
                    fname = [fname]
                if islist:
                    self.dict[a[1]] = "\n".join(a[2].format("../shared/ptxprint/{}".format(f.name)) for f in fname)
                else:
                    self.dict[a[1]] = "../shared/ptxprint/{}".format(fname.name)
        if self.dict["fancy/versedecorator"] != "%":
            self.dict["fancy/versedecoratorisfile"] = "" if self.dict["fancy/versedecoratortype"] == "file" else "%"
            self.dict["fancy/versedecoratorisayah"] = "" if self.dict["fancy/versedecoratortype"] == "ayah" else "%"
        else:
            self.dict["fancy/versedecoratorisfile"] = "%"
            self.dict["fancy/versedecoratorisayah"] = "%"
        self.dict['notes/abovenotetotal'] = f2s(float(self.dict['notes/abovenotespace'] or 0)
                                                          + float(self.dict['notes/belownoterulespace'] or 0))
        # print(", ".join("{}={}".format(a, self.dict["fancy/versedecorator"+a]) for a in ("", "type", "isfile", "isayah")))
        
        a = self.printer.get('fcb_gridOffset')
        if a == 'margin':
            vals = (self.dict["paper/margins"], self.dict["paper/topmargin"])
        else:
            vals = ("0.0", "0.0")
        (self.dict["grid/xoffset_"], self.dict["grid/yoffset_"]) = vals
        for a in ('project/frontfile', 'project/ptxprintstyfile_', 'diglot/ptxprintstyfile_'):
            if a not in self.dict:
                self.dict[a] = ''

        # handle diglot fractions
        # if self.dict['poly/fraction']:
            # self.dict['poly/fraction1'] = str(float(self.dict['poly/fraction']) / 100.)

        # Any more absolute paths?
        for a in ('diglot/ptxprintstyfile_',):
            if (len(self.dict[a])):
                    self.dict[a] = rel(self.dict[a],docdir)

        if self.dict.get('paper/cropmarks', False) and int(self.dict.get('finishing/pgsperspread', 1)) < 2:
            self.dict['paper/ifcropmarks'] = "true"
        else:
            self.dict['paper/ifcropmarks'] = "false"
        if self.dict.get('document/tocleaders', None) is None:
            self.dict['document/tocleaders'] = 0
        self.dict['document/iftocleaders'] = '' if int(self.dict['document/tocleaders'] or 0) > 0 else '%'
        self.dict['document/tocleaderstyle'] = self._tocleaders[int(self.dict['document/tocleaders'] or 0)]
        self.dict['document/tocleaderrule'] = "hrule" if int(self.dict['document/tocleaders'] or 0) == 4 else ""
        self.calcRuleParameters()
        if self.asBool('cover/includespine'):
            self.dict['cover/spinewidth_'] = float((self.dict.get("cover/spinewidth") or "0mm").replace("mm", ""))
        else:
            if self.asBool('cover/covercropmarks'):
                self.dict['cover/spinewidth_'] = 0
            else:
                self.dict['cover/spinewidth_'] = -0.1
        self.dict['project/intfile'] = ''
        if self.dict['cover/makecoverpage'] != "%":
            self.dict['transparency_'] = "false"
        p = self.dict['project/plugins'].strip()
        if len(p) and not p.strip().startswith("\\"):
            self.plugins = set(re.split("[ ,]+", p))
            self.dict['project/plugins'] = ''
        else:
            self.plugins = set()
        chvssep = self.dict['header/chvseparator']
        self.dict['chvssep_'] = self.ptsettings.get('ChapterVerseSeparator', chvssep) if chvssep == ':' else chvssep
        rsep = self.ptsettings.get('RangeIndicator', '-')
        self.dict['rangesep_'] = "\u2013" if rsep == "-" else rsep

    def updatefields(self, a):
        modelmap.get = lambda k: self[k]
        for k in a:
            v = ModelMap[k]
            val = self.printer.get(v.widget, skipmissing=k.startswith("scripts/")) if v.widget is not None else None
            if v.process is None:
                self.dict[k] = val
            else:
                try:
                    sig = signature(v.process)
                    if len(sig.parameters) == 2:
                        self.dict[k] = v.process(self.printer, val)
                    else:
                        self.dict[k] = v.process(self.printer, val, self)
                except Exception as e:
                    raise type(e)("In TeXModel with key {}, ".format(k) + str(e))
        for k, opt, wname in TeXpert.opts():
            v = self.printer.get(wname)
            self.dict["texpert/"+opt.ident] = v if opt.valfn is None else opt.valfn(v) 

    def calcRuleParameters(self):
        notemap = {'fn': 'note', 'xr': 'xref', 'sn': 'study'}
        fnrule = None
        enrule = None
        endnotes = []
        for a in ('fn', 'xr'):
            if self.dict['notes/{}pos'.format(a)] == 'endnote':
                enrule = a if enrule is None else enrule
                endnotes.append(r"\NoteAtEnd{{{}}}".format(a[0]))
            elif fnrule is None:
                fnrule = a
        for a in (('Foot', fnrule), ('End', enrule), ('Study', 'sn')):
            dat = []
            if a[1] is not None:
                pos = int(self.dict['notes/{}ruleposn'.format(a[1])] or 0)
                left = r"\hskip {:.2f} mm".format(float(self.dict['notes/{}ruleindent'.format(a[1])] or 0.))
                right = r"\hss"
                if pos == 2 or pos == 4:      # Right or Outer
                    right, left = (left, right)
                elif pos == 5:
                    left = r"\hss"
                if pos < 3 or pos == 5:         # Left, Right or Centre
                    dat.append(r"\def\{}NoteRuleLeftIndent{{{}}}".format(a[0], left))
                    dat.append(r"\def\{}NoteRuleRightIndent{{{}}}".format(a[0], right))
                else:
                    dat.append(r"\def\{}NoteRuleLeftIndent{{\ifodd\pageno {}\else {}\fi}}".format(a[0], left, right))
                    dat.append(r"\def\{}NoteRuleRightIndent{{\ifodd\pageno {}\else {}\fi}}".format(a[0], right, left))
                dat.append(r"\def\{}NoteRuleThickness{{{} pt}}".format(a[0], self.dict['notes/{}rulethick'.format(a[1])] or "0.4"))
                dat.append(r"\def\{}NoteRuleWidth{{{:.2f}}}".format(a[0], float(self.dict['notes/{}rulelength'.format(a[1])] or 100.)/100))
                bspace = float(self.dict['notes/below{}rulespace'.format(notemap[a[1]])] or 0.)
                dat.append(r"\def\Below{}NoteRuleSpace{{{:.1f} pt}}".format(a[0], bspace))
                aspace = float(self.dict['notes/above{}space'.format(notemap[a[1]])] or 0.) + bspace
                dat.append(r"\Above{}NoteSpace={:.1f} pt".format(a[0] if a[0] != "Foot" else "", aspace))
            self.dict['noterules/{}'.format(a[0].lower())] = "\n".join(dat)
        self.dict['noterules/endnotemarkers'] = "\n".join(endnotes)

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def asBool(self, key, true=None, false=None):
        val = self.dict.get(key, None)
        if val is None:
            return False
        elif true is not None:
            return val == true
        elif false is not None:
            return val != false
        elif isinstance(val, bool):
            return val
        elif val == "%" or val == "false":
            return False
        else:
            return True

    def prePrintChecks(self):
        reasons = []
        for a in ('regular', 'bold', 'italic', 'bolditalic'):
            # print("Checking {}: {}".format(a, self.dict['document/font{}'.format(a)]))
            if not self.dict['document/font{}'.format(a)]:
                reasons.append(_("Missing font ({})").format(a))
            break
        return reasons

    def processHdrFtr(self, printer):
        """ Update model headers from model UI read values """
        diglot = True if self.dict["document/ifdiglot"] == "" else False
        v = self.dict["footer/ftrcenter"]
        pri = self.dict["footer/ftrcenterside"] == "Pri" 
        t = self._hdrmappings.get(v, v)
        if diglot:
            t = self._addLR(t, pri)
            swap = False # FixMe! self.dict['document/diglotswapside'] == 'true'
            # ratio = float(self.dict['document/diglotprifraction']) # FixMe!
            ratio = 0.5
            # print(f"{ratio=}")
            if ratio > 0.5:
                lhfil = "\\ifdiglot\\ifseriesdiglot\\else\\hskip 0pt plus {}fil\\fi\\fi".format(f2s(ratio/(1-ratio)-1))
                rhfil = ""
            else:
                rhfil = "\\ifdiglot\\ifseriesdiglot\\else\\hskip 0pt plus {}fil\\fi\\fi".format(f2s((1-ratio)/ratio-1))
                lhfil = ""
        self.dict['footer/oddcenter'] = t
        self.dict['footer/evencenter'] = t
        if self.dict['footer/ifftrtitlepagenum'] == "":
            self.dict['footer/titleevencenter'] = self.dict['footer/titleoddcenter'] = self._addLR('\\pagenumber', pri)
        elif self.dict['footer/ifprintconfigname'] == "":
            self.dict['footer/titleevencenter'] = self.dict['footer/titleoddcenter'] = self.dict['config/name']
        else:
            self.dict['footer/titleevencenter'] = self.dict['footer/evencenter']
            self.dict['footer/titleoddcenter'] = self.dict['footer/oddcenter']

        mirror = self.asBool("header/mirrorlayout")
        for side in ('left', 'center', 'right'):
            v = self.dict["header/hdr"+side]
            pri = self.dict["header/hdr"+side+"side"] == "Pri"
            t = self._hdrmappings.get(v, v)
            if diglot:
                t = self._addLR(t, pri)
            self.dict['header/odd{}'.format(side)] = t
            if mirror:
                self.dict['header/even{}'.format(self._swapRL[side])] = self.mirrorHeaders(t, diglot)
            else:
                self.dict['header/even{}'.format(side)] = t

            if t.startswith((r'\first', r'\last', r'\range')): # ensure noVodd + noVeven is \empty
                self.dict['header/noVodd{}'.format(side)] = r'\empty'
            else:
                self.dict['header/noVodd{}'.format(side)] = t  # copy the other header as is
            if mirror:
                if t.startswith((r'\first', r'\last', r'\range')):
                    self.dict['header/noVeven{}'.format(self._swapRL[side])] = r'\empty'
                else:
                    self.dict['header/noVeven{}'.format(self._swapRL[side])] = self.mirrorHeaders(t, diglot)
            else:
                if t.startswith((r'\first', r'\last', r'\range')): # ensure noVodd + noVeven is \empty
                    self.dict['header/noVeven{}'.format(side)] = r'\empty'
                else:
                    self.dict['header/noVeven{}'.format(side)] = t 

            if side == "center" and diglot and self.dict["document/diglotadjcenter"]:
                for a in ('header/odd', 'header/even', 'footer/odd', 'footer/even',
                          'footer/titleeven', 'footer/titleodd', 'header/noVeven', 'header/noVodd'):
                    b = (a+"{}").format(side)
                    if 'even' in a:
                        self.dict[b] = (rhfil if mirror ^ swap else lhfil) \
                                    + self.dict[b] + (lhfil if mirror ^ swap else rhfil)
                    else:
                        self.dict[b] = (rhfil if swap else lhfil) + self.dict[b] + (lhfil if swap else rhfil)

    def _addLR(self, t, pri):
        if t in [r"\firstref", r"\lastref", r"\rangeref", r"\pagenumber", r"\hrsmins", r"\isodate" \
                 r"\book", r"\bookalt"]:                
            if pri:
                t = t+'L'
            else:
                t = t+'R'
        elif t == r"\empty":
            pass
        else:
            if pri:
                t = r"\headfootL{{{}}}".format(t)
            else:
                t = r"\headfootR{{{}}}".format(t)
        return t

    def mirrorHeaders(self, h, dig=False):
        if dig and h.endswith(("L", "R")):
            try:
                return self._mirrorRL[h[:-1]]+h[-1:]
            except KeyError:
                return h
        else:
            try:
                return self._mirrorRL[h]
            except KeyError:
                return h

    def calculateMargins(self):
        (marginmms, topmarginmms, bottommarginmms, headerposmms, footerposmms,
         ruleposmms, headerlabel, footerlabel, hfontsizemms) = self.printer.getMargins()
        self.dict["paper/topmarginfactor"] = f2s(topmarginmms / marginmms)
        self.dict["paper/bottommarginfactor"] = f2s(bottommarginmms / marginmms)
        self.dict["paper/headerposition"] = f2s(headerposmms / marginmms)
        self.dict["paper/footerposition"] = f2s(footerposmms / marginmms)
        self.dict["paper/ruleposition"] = f2s(ruleposmms * 72.27 / 25.4)
        
    def texfix(self, path):
        return path.replace(" ", r"\ ")

    def _getinsertname(self, bk):
        res = []
        bki = booknumbers.get(bk, 200)
        for b, i in self._bookinserts:
            r = [booknumbers[s] for s in b.split("-")]
            if i not in self.inserts and r[0] <= bki <= r[1]:
                if self._doperiph(i) != "":
                    self.inserts[i] = bk
                    res.append(i)
        return res

    def prep_pdfs(self, files, restag="frontIncludes_", file_dir="."):
        # for s in w.FrontPDFs) if (w.get("c_inclFrontMatter") and w.FrontPDFs is not None
        #  and w.FrontPDFs != 'None') else ""),
        if files is None:
            return
        outps = []
        for f in files:
            p = Path(f, self.printer)
            outp = str(p).replace("/", "_")
            outpath = os.path.join(file_dir, outp)
            sanitiseme = False
            if os.path.exists(outpath):
                ostat = os.stat(outpath)
                fstat = os.stat(f)
                if fstat.st_mtime > ostat.st_mtime:
                    sanitiseme = True
            else:
                sanitiseme = True
            use = outpath
            if os.path.exists(f):
                if sanitiseme:
                    if not sanitise(f.as_posix(), Path(outpath).as_posix(), forced=False):
                        use = f
            if os.path.exists(use):
                outps.append(use)
        self.dict[restag] = "\n".join('\\includepdf{{{}}}'.format(Path(s).as_posix()) for s in outps)

    def updateStyles(self):
        if self.dict['document/marginalverses'] != '%':
            self.printer.styleEditor.setval("v", "Position", self.dict["document/marginalposn"])
            self.printer.saveStyles()

    def _doptxfile(self, fname, diglots, template, beforelast, bkindex):
        res = []
        if diglots:
            res.append(r"\zglot|L\*")
        else:
            res.extend(beforelast)
        res.append(template.format(fname))
        if bkindex is None:
            return res
        if diglots:
            for k, v in self.dict['diglots_'].items():
                res.append(r"\zglot|{}\*".format(k))
                res.extend(beforelast)
                dname = v.dict['project/books'][bkindex]
                res.append(template.format(dname))
            res.append(r"\zglot|\*")
            res.append(r"\diglottrue")
        return res

    def asTex(self, template="template.tex", filedir=".", jobname="Unknown", extra="", diglots=False):
        for k, v in self._settingmappings.items():
            if self.dict[k] == "":
                self.dict[k] = self.ptsettings.dict.get(v, "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z")
        res = []
        resetPageDone = False
        docdir, docbase = self.docdir()
        digserialbooks = set((self.dict['document/diglotserialbooks'] or "").split())
        self.dict['jobname'] = jobname
        self.dict['document/imageCopyrights'] = self.generateImageCopyrightText()
                # if self.dict['document/includeimg'] else self.generateEmptyImageCopyrights()
        self.dict['project/colophontext'] = re.sub('://', ':/\u200B/\u200B', self.dict['project/colophontext']).replace("//","\u2028")
        self.dict['project/colophontext'] = re.sub(r"(?i)(\\zimagecopyrights)([A-Z]{2,3})",
                lambda m:m.group(0).lower(), self.dict['project/colophontext'])
        self.updateStyles()
        for a in (('FrontPDFs', 'c_inclFrontMatter', 'frontincludes_'),
                  ('BackPDFs', 'c_inclBackMatter', 'backincludes_')):
            files = getattr(self.printer, a[0], None)
            if files is not None and self.printer.get(a[1]):
                self.prep_pdfs(files, restag=a[2], file_dir=filedir)
            else:
                self.dict[a[2]] = ""
        if self.dict.get('fancy/enableornaments', "%") != "%":
            self.plugins.add('ornaments')
        lyt = self.dict.get('document/diglotlayout', "LR")
        if lyt is not None:
            if "/" in lyt:
                self.plugins.add('polyglot-complexpages')
                self.plugins.discard('polyglot-simplepages')
            elif "," in lyt:
                self.plugins.add('polyglot-simplepages')
        if self.dict['cover/makecoverpage'] != "%":
            self.plugins.add('cover')
        self.dict['plugins_'] = ",".join(sorted(self.plugins))
        isscripture = False
        with universalopen(os.path.join(pycodedir(), template)) as inf:
            for l in inf.readlines():
                if l.startswith(r"%\ptxfile"):
                    res.append(r"\PtxFilePath={"+saferelpath(filedir, docdir).replace("\\","/")+"/}")
                    for i, f in enumerate(self.dict['project/bookids']):
                        fname = self.dict['project/books'][i]
                        dname = None
                        beforelast = []
                        if extra != "":
                            fname = re.sub(r"^([^.]*).(.*)$", r"\1"+extra+r".\2", fname)
                        if isscripture == (f in nonScriptureBooks):
                            isscripture = not isscripture
                            res.append(r"\scripturebook{}".format("true" if isscripture else "false"))
                        if self.dict.get('project/sectintros'):
                            insertnames = self._getinsertname(f)
                            if len(insertnames):
                                if not diglots:
                                    res.append(r"\diglotfalse")
                                for ins in insertnames:
                                    res.extend(self._doptxfile(ins, diglots, 
                                            ("\\intropages{{{}}}" 
                                                if self.dict['project/periphpagebreak']
                                                else "\\prepusfm\\zgetperiph|{}\\*\\unprepusfm"), "", None))
                                if diglots:
                                    res.append(r"\diglottrue")
                        if i == len(self.dict['project/bookids']) - 1: 
                            beforelast.append(r"\lastptxfiletrue")
                            if self.dict['project/ifcolophon'] == "" and self.dict['project/pgbreakcolophon'] != '%':
                                beforelast.append(r"\endbooknoejecttrue")
                        if not resetPageDone and f not in nonScriptureBooks: 
                            if not self.dict['document/noblankpage']:
                                res.append(r"\catcode`\@=11 \need@oddpage{\emptyoutput}\catcode`\@=12")
                            res.append(r"\edef\oldpageno{\the\pageno}% Just in case the user wants it");
                            res.append(r"\pageno={}".format(self.dict['document/startpagenum']))
                            resetPageDone = True
                        if not self.asBool('document/ifshow1chbooknum') and \
                                   self.asBool('document/ifshowchapternums', '%') and f in oneChbooks:
                            res.append(r"\OneChapBooktrue")
                            res.extend(self._doptxfile(fname, diglots and f in digserialbooks, "\\ptxfile{{{}}}", beforelast, i))
                            res.append(r"\OneChapBookfalse")
                        elif self.dict['document/diffcolayout'] and \
                                    f in self.dict['document/diffcolayoutbooks']:
                            cols = self.dict['paper/columns']
                            res.append(r"\BodyColumns={}".format('2' if cols == '1' else '1'))
                            res.extend(self._doptxfile(fname, diglots and f in digserialbooks, "\\ptxfile{{{}}}", beforelast, i))
                            res.append(r"\BodyColumns={}".format(cols))
                        else:
                            res.extend(self._doptxfile(fname, diglots and f in digserialbooks, "\\ptxfile{{{}}}", beforelast, i))
                elif l.startswith(r"%\extrafont") and self.dict["document/fontextraregular"]:
                    spclChars = re.sub(r"\[uU]([0-9a-fA-F]{4,6})", lambda m:chr(int(m.group(1), 16)),
                                                                            self.dict["paragraph/missingchars"])
                    # print(spclChars.split(' '), [len(x) for x in spclChars.split(' ')])
                    if self.dict["paragraph/ifusefallback"] and len(spclChars):
                        badlist = "\u2018\u2019\u201c\u201d*#%"
                        specials = spclChars.replace(" ", "").encode("raw_unicode_escape").decode("raw_unicode_escape")
                        a = ["".join(chr(ord(c) + 16 if ord(c) < 58 else ord(c) - 23)
                             for c in str(hex(ord(x)))[2:]).lower() for x in specials]
                        b = ["".join((c) for c in str(hex(ord(x)))[2:]).lower() for x in specials]
                        c = [x for x in zip(a,b) if chr(int(x[1],16)) not in badlist]
                        if not len(c):
                            continue
                        res.append(r"% for defname @active+ @+digit => 0->@, 1->a ... 9->i A->j B->k .. F->o")
                        res.append(r"% 12 (size) comes from \p size")
                        res.append(r'\def\extraregular{{"{}"}}'.format(self.dict["document/fontextraregular"]))
                        res.append(r"\catcode`\@=11")
                        res.append(r"\def\do@xtrafont{\x@\s@textrafont\ifx\thisch@rstyle\undefined\m@rker\else\thisch@rstyle\fi}")
                        for a,b in c:
                            res.append(r"\def\@ctive{}{{\leavevmode{{\do@xtrafont {}{}}}}}".format(a, '^'*len(b), b))
                            res.append(r"\DefineActiveChar{{{}{}}}{{\@ctive{}}}".format( '^'*len(b), b, a))
                        res.append(r"\activ@tecustomch@rs")
                        res.append(r"\catcode`\@=12")
                    else:
                        res.append(r"% No special/missing characters specified for fallback font")
                elif l.startswith(r"%\horiznotespacing"):
                    mins = float(self.dict["notes/horiznotespacemin"])
                    maxs = float(self.dict["notes/horiznotespacemax"])
                    tgts = mins + ((maxs - mins) / 3)
                    minus = tgts - mins
                    plus = maxs - tgts
                    res.append(r"\internoteskip={}pt plus {}pt minus {}pt".format(f2s(tgts), f2s(plus), f2s(minus)))
                elif l.startswith(r"%\optimizepoetry"):
                    bks = self.dict["document/clabelbooks"]
                    if self.dict["document/ifchaplabels"] == "%" and len(bks):
                        for bk in bks.split(" "):
                            if bk in self.dict['project/bookids']:
                                res.append((r"\setbookhook{{start}}{{{}}}{{\xdef\lBalThresh{{\BalanceThreshold}}\gdef\BalanceThreshold{{3}}\clubpenalty=50"
                                            + r"\widowpenalty=50}}").format(bk))
                                res.append((r"\setbookhook{{end}}{{{}}}{{\gdef\BalanceThreshold{{\lBalThresh}}\clubpenalty=10000"
                                            + r"\widowpenalty=10000}}").format(bk))
                elif l.startswith(r"%\snippets"):
                    for t in self.tablespans:
                        res.append(r"\spanningcols{{{}}}{{{}}}{{{}}}{{{}}}".format(*t))
                    for k, c in sorted(self._snippets.items(), key=lambda x: x[1][2].order):
                        if c[1] is None:
                            v = self.asBool(k)
                        else:
                            v = c[1](self.dict[k])
                        if v:
                            fn = getattr(c[2], 'generateTex', None)
                            if fn is not None:
                                res.append(fn(v, self))
                            elif c[2].processTex:
                                res.append(c[2].texCode.format(**self.dict))
                            else:
                                res.append(c[2].texCode)
                    script = self.dict["document/script"]
                    if len(script) > 0:
                        sclass = getattr(scriptsnippets, script[8:].lower(), None)
                        if sclass is not None:
                            res.append(sclass.tex(self.printer))
                    res.append("""
\\catcode"FDEE=1 \\catcode"FDEF=2
\\prepusfm
\\def\\zcopyright\uFDEE{project/copyright}\uFDEF
\\def\\zlicense\uFDEE{project/license}\uFDEF
""".format(**self.dict))
                    if "diglot/copyright" in self.dict:
                        res.append("\\def\\zcopyrightR\uFDEE{}\uFDEF".format(self.dict["diglot/copyright"]))
                    res.append("\\unprepusfm")
                    res.append("\n%% Advanced TeXpert options")
                    res.append(TeXpert.generateTeX(self.printer))
                elif l.startswith(r"%\defzvar"):
                    for k in self.printer.allvars():
                        res.append(r"\defzvar{{{}}}{{{}}}".format(k, texprotect(self.printer.getvar(k))))
                    for k, e in (('toctitle', 'document/toctitle'),):
                        res.append(r"\defzvar{{{}}}{{{}}}".format(k, texprotect(self.dict[e])))
                elif l.startswith(r"%\diglot "):
                    if diglots:
                        l = l[9:]
                        # breakpoint()
                        for a, digdict in self.dict["diglots_"].items():
                            res.append(l.strip().format(diglot=digdict.dict, s_=a, **self.dict))
                else:
                    res.append(l.rstrip().format(**self.dict))
        return "\n".join(res).replace("\\OneChapBookfalse\n\\OneChapBooktrue\n","")

    def _doperiph(self, k):
        if self.frontperiphs is None or not len(self.frontperiphs):
            self.frontperiphs = {}
            for a in ('FRT', 'INT'):
                frtfile = os.path.join(self.printer.project.path, self.printer.getBookFilename(a))
                logger.debug(f"Trying periphs file {frtfile}")
                if not os.path.exists(frtfile):
                    continue
                with open(frtfile, encoding="utf-8") as inf:
                    mode = 0        # default
                    currperiphs = []
                    currk = None
                    for l in inf.readlines():
                        l = runChanges(self.changes.get('periph', self.changes.get('default', [])), a, l)
                        logger.log(5, f"{mode}: {l}")
                        ma = re.match(r'\\periph\s*([^|]*)(?:\|\s*(?:id\s*=\s*"([^"]+)|(\S+)))?', l)
                        if ma:
                            if mode == 1:    # already collecting so save
                                self.frontperiphs[currk] = "\n".join(currperiphs)
                            currk = ma[2] or ma[3]
                            if not currk:
                                t = ma[1].strip().lower()
                                currk = _periphids.get(t, t)
                            currperiphs = [l.rstrip()]
                            mode = 1
                        elif mode == 1:
                            if r"\periph" in l:
                                mode = 0
                            else:
                                currperiphs.append(l.rstrip())
                    if currk is not None:
                        self.frontperiphs[currk] = "\n".join(currperiphs)
                        # print(f"{currk=}\n{self.frontperiphs[currk]=}")
            logger.debug(f"Contains periphs: {sorted(self.frontperiphs.keys())}")
        return self.frontperiphs.get(k, f"\\rem zgetperiph|{k}\\*")

    def createFrontMatter(self, outfname):
        self.dict['project/frontfile'] = os.path.basename(outfname)
        infpath = self.printer.configFRT()
        logger.debug(f"Using front matter from {infpath}")
        bydir = os.path.join(pycodedir(), "images").replace("\\", "/")
        fmt = self.dict['snippets/pdfoutput']
        cmyk = fmt in ('CMYK', 'PDF/X-1A', 'PDF/A-1')
        if os.path.exists(infpath):
            fcontent = []
            with open(infpath, encoding="utf-8") as inf:
                for l in inf.readlines():
                    l = runChanges(self.changes.get('periph', self.changes.get('default', [])), "FRT", l)
                    if re.match(r"^\s*\\rem\s", l.lower()):
                        continue
                    l = re.sub(r"\\zgetperiph\s*\|([^\\\s]+)\s*\\\*", lambda m:self._doperiph(m[1]), l)
                    l = re.sub(r"\\zbl\s*\|(\d+)\\\*", lambda m: "\\b\n" * int(m.group(1)), l)
                    l = re.sub(r"\\zccimg\s*(.*?)(?:\|(.*?))?\\\*",
                            lambda m: r'\fig |src="'+bydir+"/"+m.group(1)+("_cmyk" if cmyk else "") \
                                     + '.jpg" copy="None" ' + m.group(2)+ r'\fig*', l)
                    l = re.sub(r'(\\fig .*?src=")(.*?)(".*?\\fig\*)', lambda m:m.group(1)+m.group(2).replace("\\","/")+m.group(3), l)
                    fcontent.append(l.rstrip())
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write("\n".join(fcontent))

    def addInt(self, outfname):
        intfname = self.printer.getBookFilename('INT')
        if intfname is None or not len(intfname):
            return
        intfile = os.path.join(self.printer.project.path, intfname)
        def addperiphid(m):
            if m.group(2).lower() in _periphids:
                return m.group(1) + f'|id="{_periphids[m.group(2).lower()]}"\n'
            else:
                return m.group(1)+"\n"
        if os.path.exists(intfile):
            self.dict['project/intfile'] = "\\ptxfile{{{}}}".format(os.path.basename(outfname))
            with open(intfile, encoding="utf-8") as inf:
                dat = inf.read()
            dat = runChanges(self.changes.get('periph', self.changes.get('default', [])), "INT", dat)
            dat = runChanges(self.localChanges or [], "INT", dat)
            dat = regex.sub(r"(\\periph\s*([^\n|]+))\n", addperiphid, dat)
            with open(outfname, "w", encoding="utf-8") as outf:
                outf.write(dat)
        logger.debug(f"INT file {intfname} processed to {outfname}")
        return outfname

    def flattenModule(self, infpath, outdir, text=None):
        outfpath = os.path.join(outdir, os.path.basename(infpath))
        doti = outfpath.rfind(".")
        if doti > 0:
            outfpath = outfpath[:doti] + "-flat" + outfpath[doti:]
        usfms = self.printer.get_usfms()
        try:
            mod = Module(infpath, usfms, self, text=text)
            mod.parse()
            res = mod.doc
        except SyntaxError as e:
            return (None, e)
        if text is not None:
            return res
        res.xml.outUsfm(outfpath)
        return outfpath

    def runConversion(self, infpath, outdir):
        outfpath = infpath
        script = self.dict['project/selectscript']
        if self.dict['project/processscript'] and script and os.path.exists(script):
            outfpath = os.path.join(outdir, os.path.basename(infpath))
            doti = outfpath.rfind(".")
            if doti > 0:
                outfpath = outfpath[:doti] + "-conv" + outfpath[doti:]
            cmd = [script, infpath, outfpath]
            if script.lower().endswith(".bat") and sys.platform.startswith("win"):
                cmd = [os.environ.get('COMSPEC', 'cmd.exe'), '/c'] + cmd
            else:
                hasrun = False
                with open(script, encoding="utf-8") as scriptf:
                    l = scriptf.readline().replace("\uFEFF", "")
                    if script.lower().endswith(".py") or re.match(r"^#!.*?(?<=[ /!])python", l):
                        scriptf.seek(0)
                        gs = globals().copy()
                        gs["__name__"] = "__main__"
                        sys._argv = sys.argv
                        sys.argv = [script, infpath, outfpath]
                        # "Remember that at the module level, globals and locals are the same dictionary.
                        # If exec gets two separate objects as globals and locals, the code will be executed
                        # as if it were embedded in a class definition."
                        exec(scriptf.read(), gs)
                        sys.argv = sys._argv
                        hasrun = True
            if not hasrun:
                checkoutput(cmd) # dont't pass cmd as list when shell=True
        return outfpath

    def _getText(self, data, doc, bk, logmsg=""):
        if doc is not None:
            data = doc.asUsfm(grammar=self.printer.usfms.grammar)
            logger.log(5, logmsg+data)
        return (data, None)

    def _getDoc(self, data, doc, bk, logmsg=""):
        if data is not None:
            doc = self._makeUSFM(data, bk)
            doc.xml.version="3.1"
            if doc is not None:
                logger.log(5, logmsg+doc.outUsx(None))
        return (None if doc else data, doc)
        
    def _changeError(self, txt):
        self.printer.doError(txt + "\n\n" +_("If this error just appeared after upgrading then check whether the USFM markers like \\p and \\v used in changes.txt rules have been 'escaped' with an additional \\ (e.g. \\\\p and \\\\v) as is required by the latest version."), title="Error in changes.txt")
        logger.warn(txt)

    def convertBook(self, bk, chaprange, outdir, prjdir, isbk=True, bkindex=0, reversify=None):
        try:
            isCanon = int(bookcodes.get(bk, 100)) < 89
        except ValueError:
            isCanon = False
        printer = self.printer
        if not len(self.changes):
            if self.asBool('project/usechangesfile'):
                # print("Applying PrntDrftChgs:", os.path.join(prjdir, 'PrintDraftChanges.txt'))
                #cpath = self.printer.configPath(self.printer.configName())
                #self.changes = self.readChanges(os.path.join(cpath, 'changes.txt'), bk)
                self.changes = self.readChanges(os.path.join(printer.project.srcPath(printer.cfgid), 'changes.txt'), bk)
        #adjlistfile = printer.getAdjListFilename(bk)
        #if adjlistfile is not None:
        #    adjchangesfile = os.path.join(printer.project.srcPath(printer.cfgid), "AdjLists",
        #                        adjlistfile.replace(".adj", "_changes.txt"))
        #    chs = self.readChanges(adjchangesfile, bk, makeranges=True, passes=["adjust"])
        #    for k, v in chs.items():
        #        self.changes.setdefault(k, []).extend(v)
        draft = "-" + (printer.cfgid or "draft")
        self.makelocalChanges(printer, bk, chaprange=(chaprange if isbk else None))
        customsty = os.path.join(prjdir, 'custom.sty')
        if not os.path.exists(customsty):
            self.dict["/nocustomsty"] = "%"
        else:
            self.dict["/nocustomsty"] = ""
        fname = printer.getBookFilename(bk)
        if fname is None:
            infpath = os.path.join(prjdir, bk)  # assume module
            infpath = self.flattenModule(infpath, outdir)
            if isinstance(infpath, tuple) and infpath[0] is None:
                self.printer.doError("Failed to flatten module text (due to a Syntax Error?):",        
                        secondary=str(infpath[1]), 
                        title="PTXprint [{}] - Canonicalise Text Error!".format(self.VersionStr),
                        show=not self.printer.get("c_quickRun"))
                return None
        else:
            infpath = os.path.join(prjdir, fname)
        if self.dict['project/processscript'] and self.dict['project/when2processscript'] == "before":
            infpath = self.runConversion(infpath, outdir)
        outfname = os.path.basename(infpath)
        outindex = self.usedfiles.setdefault(outfname, 0)
        outextra = str(outindex) if outindex > 0 else ""
        self.usedfiles[outfname] = outindex + 1
        # outfname = fname
        doti = outfname.rfind(".")
        if doti > 0:
            outfname = outfname[:doti] + draft + outextra + outfname[doti:]
        os.makedirs(outdir, exist_ok=True)
        outfpath = os.path.join(outdir, outfname)
        codepage = self.ptsettings.get('Encoding', 65001)
        with universalopen(infpath, cp=codepage) as inf:
            dat = inf.read()
        doc = None
        logger.debug(f"Converting {bk} {chaprange=} sections{self.changes.keys()}")

        if 'initial' in self.changes:
            (dat, doc) = self._getText(dat, doc, bk, logmsg="Unparsing doc to run user changes\n")
            dat = runChanges(self.changes['initial'], bk, dat, errorfn=self._changeError if bkindex == 0 else None)

        if chaprange is None and self.dict["project/bookscope"] == "single":
            chaprange = RefList((RefRange(Reference(bk, int(float(self.dict["document/chapfrom"])), 0),
                                 Reference(bk, int(float(self.dict["document/chapto"])), 200)), ))

        logger.debug(f"Converting {bk} {chaprange=}")
        if chaprange is None or not isbk or not len(chaprange) or \
            (chaprange[0].first.chapter < 2 and len(chaprange) == 1 and \
                (chaprange[0].last.chapter >= int(chaps[bk]) or chaprange[0].last.chapter == 0)):
            doc = None
        else:
            (dat, doc) = self._getDoc(dat, doc, bk)
            if doc is not None:
                doc = doc.getsubbook(chaprange)

        if self.interlinear is not None:
            (dat, doc) = self._getText(dat, doc, bk)
            linelengths = [len(x) for x in dat.splitlines(True)]
            (dat, doc) = self._getDoc(dat, doc, bk)
            if doc is not None:
                self.interlinear.convertBk(bk, doc, keep_punct = self.dict.get("project/interpunc", True))
                if len(self.interlinear.fails):
                    refs = RefList(self.interlinear.fails)
                    refs.simplify()
                    printer.doError("The following references need to be reapproved: " + str(refs),
                                    show=not printer.get("c_quickRun"))
                    self.interlinear.fails = []
        elif bk.lower().startswith("xx"):
            (dat, doc) = self._getText(dat, doc, bk, logmsg="flatten the module")
            doc = self.flattenModule(infpath, outfpath, text=dat)
            dat = None

        if 'default' in self.changes:
            (dat, doc) = self._getText(dat, doc, bk, logmsg="Unparsing doc to run user changes\n")
            dat = runChanges(self.changes['default'], bk, dat, errorfn=self._changeError if bkindex == 0 else None)

        if self.dict['project/canonicalise']:
            (dat, doc) = self._getDoc(dat, doc, bk)
            dat = None

        if not self.asBool("document/bookintro") or not self.asBool("document/introoutline"):
            (dat, doc) = self._getDoc(dat, doc, bk)
            logger.debug("stripIntro")
            if doc is not None:
                doc.stripIntro(not self.asBool("document/bookintro"), not self.asBool("document/introoutline"))

        if self.asBool("document/hidemptyverses"):
            (dat, doc) = self._getDoc(dat, doc, bk)
            logger.debug("stripEmptyChVs")
            if doc is not None:
                doc.stripEmptyChVs(ellipsis=self.asBool("document/elipsizemptyvs"))

        if self.dict['fancy/endayah'] == "":
            (dat, doc) = self._getDoc(dat, doc, bk)
            logger.debug("versesToEnd")
            if doc is not None:
                doc.versesToEnd()

        if bk == "GLO" and self.found_glosses is not None:
            (dat, doc) = self._getDoc(dat, doc, bk, logmsg="Remove filtered gloss entries")
            if doc is not None:
                doc.removeGlosses(self.found_glosses)

        if self.dict["strongsndx/showintext"] and self.dict["notes/xrlistsource"].startswith("strongs") \
                    and self.dict["notes/ifxrexternalist"] and isCanon:
            (dat, doc) = self._getDoc(dat, doc, bk)
            logger.debug("Add strongs numbers to text")
            try:
                doc.addStrongs(printer.getStrongs(), self.dict["strongsndx/showall"])
            except SyntaxError as e:
                self.printer.doError("Processing Strongs", secondary=str(e))

        if self.asBool("paragraph/ifhyphenate") and self.asBool("document/ifletter") and printer.hyphenation:
            (dat, doc) = self._getDoc(dat, doc, bk)
            logger.debug("Insert hyphens manually")
            if doc is not None:
                doc.hyphenate(printer.hyphenation, self.dict["paragraph/ifnbhyphens"])

        if reversify is not None:
            (dat, doc) = self._getDoc(dat, doc, bk, "Prepare to reversify")
            if doc is not None:
                srcvrsf = None
                srcvrs = None
                if self.printer.ptsettings.versification is not None:
                    srcvrsf = os.path.join(self.printer.project.path, self.printer.ptsettings.versification)
                    logger.debug(f"{srcvrsf=}")
                    if os.path.exists(srcvrsf):
                        srcvrs = Versification(srcvrsf)
                logger.debug(f"Reversify [{srcvrsf}] {getattr(reversify[0], 'name', 'unknown')} -> {getattr(srcvrs, 'name', 'unknown') if srcvrs else 'unknown'}")
                doc.reversify(srcvrs, *reversify)

        if self.localChanges is not None:
            (dat, doc) = self._getText(dat, doc, bk, logmsg="Unparsing doc to run local changes\n")
            logger.log(5,self.localChanges)
            dat = runChanges(self.localChanges, bk, dat)

        adjlist = self.printer.get_adjlist(bk)
        if adjlist is not None:
            (dat, doc) = self._getDoc(dat, doc, bk)
            logger.debug("Apply adjlist")
            if doc is not None:
                doc.apply_adjlist(bk, adjlist)
            # dat = runChanges(self.changes['adjust'], bk, dat, errorfn=self._changeError if bkindex == 0 else None)

        logger.debug("Applying final changes: ")
        if 'final' in self.changes:
            (dat, doc) = self._getText(dat, doc, bk, logmsg="Unparsing doc to run user changes (final)\n")
            dat = runChanges(self.changes['final'], bk, dat, errorfn=self._changeError if bkindex == 0 else None)

        (dat, doc) = self._getText(dat, doc, bk, logmsg="Unparsing doc to output\n")
        with open(outfpath, "w", encoding="utf-8") as outf:
            outf.write(dat)
        if self.dict['project/processscript'] and self.dict['project/when2processscript'] == "after":
            bn = os.path.basename(self.runConversion(outfpath, outdir))
        else:
            bn = os.path.basename(outfpath)

        if '-conv' in bn:
            newname = re.sub(r"(\{}\-conv|\-conv\{}|\-conv)".format(draft, draft), draft, bn)
            copyfile(os.path.join(outdir, bn), os.path.join(outdir, newname))
            os.remove(os.path.join(outdir, bn))
            return newname
        else:
            return bn
            
    def _makeUSFM(self, txt, bk):
        # import pdb; pdb.set_trace()
        syntaxErrors = []
        try:
            doc = Usfm.readfile(txt, grammar=self.printer.get_usfms().grammar)
            doc.xml.canonicalise(version="3.1")
        except SyntaxError as e:
            syntaxErrors.append("{} {} line:{}".format(self.prjid, bk, str(e).split('line', maxsplit=1)[1]))
        except Exception as e:
            syntaxErrors.append("{} {} Error({}): {}".format(self.prjid, bk, type(e), str(e)))
            traceback.print_exc()
        if len(syntaxErrors):
            dlgtitle = "PTXprint [{}] - USFM Text Error!".format(self.VersionStr)
            # print(syntaxErrors[0])
            # logger.info(syntaxErrors[0])
            errbits = re.match(r"(\S+) (...) line: (\d+),\d+\s*\[(.*?)\]: orphan marker (\\.+?)", syntaxErrors[0])
            if errbits is not None:
                self.printer.doError("Syntax Error warning: ",        
                    secondary=_("Examine line {} in {} on the 'Final SFM' tab of the View+Edit " + \
                        "page to determine the cause of this issue related to marker: {} as found in the markers: {}.").format(
                                errbits[3], errbits[2], errbits[5], errbits[4]) + \
                        "\n\n"+_("This warning was triggered due to 'Auto-Correct USFM' being " + \
                        "enabled on the Advanced tab but is due to an orphaned marker. " + \
                        "It means the marker does not belong in that position, or it " + \
                        "is missing a valid parent marker."), title=dlgtitle,
                        show=not self.printer.get("c_quickRun"))
            else:
                prtDrft = _("And check if a faulty rule in changes.txt has caused the error(s).") if self.asBool("project/usechangesfile") else ""
                self.printer.doError(_("Failed to normalize texts due to a Syntax Error: "),        
                    secondary="\n".join(syntaxErrors)+"\n\n"+_("Run the Basic Checks in Paratext to ensure there are no Marker errors "+ \
                    "in either of the diglot projects. If this error persists, try running the Schema Check in Paratext as well.") + " " + prtDrft,
                    title=dlgtitle, show=not self.printer.get("c_quickRun"))
                    
            return None
        else:
            return doc  

    def make_contextsfn(self, bk, *changes):
        # functional programmers eat your hearts out
        def makefn(reg, currfn):
            if currfn is not None:
                def compfn(fn, b, s):
                    def domatch(m):
                        return currfn(lambda x:fn(m.group(0)), b, m.group(0))
                    return reg.sub(domatch, s) if bk is None or b == bk else s
            else:
                def compfn(fn, b, s):
                    return reg.sub(lambda m:fn(m.group(0)), s) if bk is None or b == bk else s
            return compfn
        return reduce(lambda currfn, are: makefn(are, currfn), reversed([c for c in changes if c is not None]), None)

    def readChanges(self, fname, bk, makeranges=False, passes=None):
        changes = {}
        if passes is None:
            passes = ["default"]
        if not os.path.exists(fname):
            return {}
        logger.debug("Reading changes file: "+fname)
        usfm = None
        if makeranges:
            try:
                usfm = self.printer.get_usfm(bk)
            except SyntaxError:
                pass
            if usfm is not None:
                usfm.addorncv()
        qreg = r'(?:"((?:[^"\\]|\\.)*?)"|' + r"'((?:[^'\\]|\\.)*?)')"
        with universalopen(fname) as inf:
            alllines = list(inf.readlines())
            i = 0
            while i < len(alllines):
                l = alllines[i].strip().replace(u"\uFEFF", "")
                i += 1
                while l.endswith("\\") and i < len(alllines):
                    l = l[:-1] + alllines[i].strip()
                    i += 1
                l = re.sub(r"\s*#.*$", "", l)
                if not len(l):
                    continue
                contexts = []
                atcontexts = []
                m = re.match(r"^\s*sections\s*\((.*?)\)", l)
                if m:
                    ts = m.group(1).split(",")
                    passes = [t.strip(' \'"') for t in ts]  # don't require ""
                    for p in passes:
                        if p not in changes:
                            changes[p] = []
                    continue
                m = re.match(r"^\s*include\s+(['\"])(.*?)\1", l)
                if m:
                    lchs = self.readChanges(os.path.join(os.path.dirname(fname), m.group(2)), bk, passes=passes, makeranges=makeranges)
                    for k, v in lchs.items():
                        changes.setdefault(k, []).extend(v)
                    continue
                # test for "at" command
                m = re.match(r"^\s*at\s+(.*?)\s+(?=in|['\"])", l)
                if m:
                    atref = RefList.fromStr(m.group(1), context=AnyBooks)
                    for r in atref.allrefs():
                        if r.chapter == 0:
                            atcontexts.append((r.book, None))
                        elif r.verse == 0:
                            atcontexts.append((r.book, regex.compile(r"(?<=\\c {}\D).*?(?=$|\\[cv]\s)".format(r.chapter), flags=regex.S)))
                        else:
                            v = None
                            if r.first != r.last:
                                v = r
                            elif usfm is not None:
                                v = usfm.bridges.get(r, r)
                                if v.first == v.last:
                                    v = None
                            if v is None:
                                outv = '{}{}'.format(r.verse, r.subverse or "")
                            else:
                                outv = "{}{}-{}{}".format(v.first.verse, v.first.subverse or "", v.last.verse, v.last.subverse or "")
                            atcontexts.append((r.book, regex.compile(r"\\c {}\D(?:[^\\]|\\(?!c\s))*?\K\\v {}\D.*?(?=$|\\[cv]\s)".format(r.chapter, outv), flags=regex.S|regex.V1)))
                    l = l[m.end():].strip()
                else:
                    atcontexts = [None]
                # test for 1+ "in" commands
                while True:
                    m = re.match(r"^\s*in\s+"+qreg+r"\s*:\s*", l)
                    if not m:
                        break
                    try:
                        contexts.append(regex.compile(m.group(1) or m.group(2), flags=regex.M))
                    except re.error as e:
                        self.printer.doError("Regular expression error: {} in changes file at line {}".format(str(e), i+1),
                                             show=not self.printer.get("c_quickRun"))
                        break
                    l = l[m.end():].strip()
                # capture the actual change
                m = re.match(r"^"+qreg+r"\s*>\s*"+qreg, l)
                if m:
                    try:
                        r = regex.compile(m.group(1) or m.group(2), flags=regex.M)
                        # t = regex.template(m.group(3) or m.group(4) or "")
                    except (re.error, regex._regex_core.error) as e:
                        self.printer.doError("Regular expression error: {} in changes file at line {}".format(str(e), i+1))
                        continue
                    for at in atcontexts:
                        if at is None:
                            context = self.make_contextsfn(None, *contexts) if len(contexts) else None
                        elif len(contexts) or at[1] is not None:
                            context = self.make_contextsfn(at[0], at[1], *contexts)
                        else:
                            context = at[0]
                        ch = (context, r, m.group(3) or m.group(4) or "", f"{fname} line {i+1}")
                        for p in passes:
                            changes.setdefault(p, []).append(ch)
                        logger.log(7, f"{context=} {r=} {m.groups()=}")
                    continue
                elif len(l):
                    logger.warning(f"Faulty change line found in {fname} at line {i}:\n{l}")
        return changes

    def makelocalChanges(self, printer, bk, chaprange=None):
        #self.changes.append((None, regex.compile(r"(?<=\\[^\\\s]+)\*(?=\S)", flags=regex.S), "* "))
        # if self.printer is not None and self.printer.get("c_tracing"):
            # print("List of changes.txt:-------------------------------------------------------------")
            # report = "\n".join("{} -> {}".format(p[1].pattern, p[2]) for p in self.changes)
            # if getattr(self.printer, "logger", None) is not None:
                # self.printer.logger.insert_at_cursor(v)
            # else:
                # try:
                    # print(report)
                # except UnicodeEncodeError:
                    # print("Unable to print details of changes.txt")
        self.localChanges = []
        script = self.dict["document/script"]
        if len(script):
            sscript = getattr(scriptsnippets, script[8:].lower(), None)
            if sscript is not None:
                self.localChanges.extend(sscript.regexes(self.printer))
        if bk == "GLO":
            if self.dict['document/filterglossary']:
                self.filterGlossary(printer)
            def mkkid(m):
                if ' ' in m.group(1):
                    return r'\k {}|{}\k*'.format(m.group(1), m.group(1).replace(" ", ""))
                else:
                    return r'\k {}\k*'.format(m.group(1))
            self.localChanges.append(makeChange(r"\\k\s+([^|\\]+)\s*(?=\\)\\k\*", mkkid, flags=regex.S))
        
        # Fix things that other parsers accept and we don't
        self.localChanges.append(makeChange(r"(\\[cv] [^ \\\r\n]+)(\\)", r"\1 \2", flags=regex.S))
        
        # Remove the \ref ... \ref* which is often inserted for \xt fields in DBL projects.
        if self.asBool('texpert/removextreflinks'):
            self.localChanges.append(makeChange(r'\\ref (.+?)\|loc=".+?"\\ref\*', r"\1", flags=regex.S))
        
        # Remove empty \h markers (might need to expand this list and loop through a bunch of markers)
        self.localChanges.append(makeChange(r"(\\h ?\r?\n)", r"", flags=regex.S))

        sliceRef = self.dict['slice/ref'] or ""
        foundSlice = False
        if len(sliceRef):
            match = bcvref.match(sliceRef)
            if match and len(self.dict['slice/word']):
                foundSlice = True
                b,c,v = match.groups()
                endc = int(c) + int(self.dict['slice/length'])
                self.localChanges.append(makeChange(rf"\\c {c}\s.+?\\v {v}\s.+?({self.dict['slice/word']})", \
                                                    rf"\uFFFF\n\{self.dict['slice/marker']} \1", flags=regex.S))
                self.localChanges.append(makeChange(r"\\mt\d?\s*.+\uFFFF\n", rf'\\zsetref|bkid="{b}" chapter="{c}" verse="{v}"\*\n', flags=regex.S))
            else:
                try:
                    startc = int(sliceRef.split(" ",1)[-1])
                    if startc > 0:
                        foundSlice = True
                        self.localChanges.append(makeChange(rf"\\mt\d?\s*.+(\\c {startc}\s)", r"\1", flags=regex.S))
                        endc = int(startc) + int(self.dict['slice/length'])
                except ValueError:
                    pass
            if foundSlice:
                self.localChanges.append(makeChange(rf"\\c {endc}\s.+", "", flags=regex.S))
        
        # This section handles PARTIAL books (from chapter X to chapter Y)
        if self.asBool("document/ifchaplabels", true="%"):
            clabel = self.dict["document/clabel"]
            clbooks = self.dict["document/clabelbooks"].split()
            if len(clabel) and (not len(clbooks) or bk in clbooks):
                self.localChanges.append(makeChange(r"(\\c )", r"\\cl {}\n\1".format(clabel), flags=regex.S))
                
        # If each chapter needs to start on a new page
        if self.asBool("document/pagebreakallchs"):
            self.localChanges.append(makeChange(r"\\c (?!1\D)", r"\\pb\n\\c ", flags=regex.S))
            pass

        # Throw out the known "nonpublishable" markers and their text (if any)
        self.localChanges.append(makeChange(r"\\(usfm|ide|rem|sts|restore|pubinfo)( .*?)?\n(?=\\)", ""))

        # Throw out any empty footnotes or cross-references (if any) even if they have an xo or fr but no content
        # e.g.  \f + \f*     \x +\x*    \f + \fr 27:12 \ft \f*    \x - \xo 27:13-15 \xt \x*    \x - \xo 27:12 \xo*\xt \xt*\x*
        self.localChanges.append(makeChange(r"\\(f|fe|ef|x)\s+\S+?\s*(\\(xo|fr)\s+[^\\]+|\\\S+\s*)*?\\\1\*", ""))

        # Remove notes if not included
        if self.asBool("notes/includefootnotes"):
            self.localChanges.append(makeChange(r"\\f\s+.*?\\f\*", ""))

        if self.asBool("notes/includexrefs"):
            self.localChanges.append(makeChange(r"\\x\s+.*?\\x\*", ""))

        ############ Temporary (to be removed later) ########%%%%
        # Throw out \esb ... \esbe blocks if Study Bible Sidebars are not wanted
        if not self.asBool("studynotes/includesidebar"):
            self.localChanges.append(makeChange(r"\\esb.+?\\esbe", "", flags=regex.S))
        ############ Temporary (to be removed later) ########%%%%
        
        if self.asBool("studynotes/includextfn"):
            if self.dict["studynotes/showcallers"] == "%":
                self.localChanges.append(makeChange(r"\\ef \- ", r"\\ef + ", flags=regex.S))
            else:
                self.localChanges.append(makeChange(r"\\ef . ", r"\\ef - ", flags=regex.S))
        else:
            self.localChanges.append(makeChange(r"\\ef( .*?)\\ef\*", "", flags=regex.S))

        if self.asBool("notes/showextxrefs"):
            self.localChanges.append(makeChange(r"\\ex", r"\\x", flags=regex.S))
        else:
            self.localChanges.append(makeChange(r"\\ex( .*?)\\ex\*", "", flags=regex.S))
        
        # If a printout of JUST the book introductions is needed (i.e. no scripture text) then this option is very handy
        if not self.asBool("document/ifmainbodytext"):
            self.localChanges.append(makeChange(r"\\c .+", "", flags=regex.S))

        # Probably need to make this more efficient for multi-book and lengthy glossaries (cache the GLO & changes reqd etc.)
        if self.asBool("notes/glossaryfootnotes"):
            self.makeGlossaryFootnotes(printer, bk)

        # Glossary Word markup: Remove the second half of the \w word|glossary-form\w* and apply chosen glossary markup
        v = self.dict["document/glossarymarkupstyle"]
        gloStyle = self._glossarymarkup.get(v, v)
        if v is not None and v != 'ai':
            if gloStyle is not None and len(v) == 2: # otherwise skip over OLD Glossary markup definitions
                self.localChanges.append(makeChange(r"\\\+?w ([^|]+?)(\|[^|]+?)?\\\+?w\*", gloStyle, flags=regex.M))

        if self.asBool("document/ifinclfigs") and bk in nonScriptureBooks:
            # Remove any illustrations which don't have a |p| 'loc' field IF this setting is on
            if self.asBool("document/iffigexclwebapp"):
                self.localChanges.append(makeChange(r'(?i)\\fig ([^|]*\|){3}([aw]+)\|[^\\]*\\fig\*', '', flags=regex.M))  # USFM2
                self.localChanges.append(makeChange(r'(?i)\\fig [^\\]*\bloc="[aw]+"[^\\]*\\fig\*', '', flags=regex.M))    # USFM3
            def figtozfiga(m):
                a = self.printer.picinfos.getAnchor(m.group(1), bk + (self.printer.digSuffix or ""))
                if a is None:
                    return ""
                ref = re.sub(r"^\S+\s+", r"", a)
                if ref.startswith("k."):
                    return ""
                return r"\zfiga|{}\*".format(ref)
            logger.debug(self.printer.picinfos)
            self.localChanges.append(makeChange(r'\\fig.*?src="([^"]+?)".*?\\fig\*', figtozfiga, flags=regex.M))
            self.localChanges.append(makeChange(r'\\fig(?: .*?)?\|(.*?)\|.*?\\fig\*', figtozfiga, flags=regex.M))

            if self.asBool("document/iffighiderefs"): # del ch:vs from caption 
                self.localChanges.append(makeChange(r"(\\fig [^\\]+?\|)([0-9:.\-,\u2013\u2014]+?)(\\fig\*)", r"\1\3", flags=regex.M))   # USFM2
                self.localChanges.append(makeChange(r'(\\fig .+?)(ref=\"\d+[:.]\d+([-,\u2013\u2014]\d+)?\")(.*?\\fig\*)', r"\1\4", flags=regex.M))   # USFM3
        else:
            # Strip out all \figs from the USFM as an internally generated temp PicList will do the same job
            self.localChanges.append(makeChange(r'\\fig[\s|][^\\]+?\\fig\*', "", flags=regex.M))

        if not self.asBool("document/sectionheads"): # Drop ALL Section Headings (which also drops the Parallel passage refs now)
            self.localChanges.append(makeChange(r"\\[sr]\d? .+", "", flags=regex.M))

        if not self.asBool("document/parallelrefs"): # Drop ALL Parallel Passage References
            self.localChanges.append(makeChange(r"\\r .+", "", flags=regex.M))

        if self.asBool("document/preventorphans"): # Prevent orphans at end of *any* paragraph (TO DO: make len of short word a parameter in TeXhacks)
            if int(self.dict['texpert/ptxversion']) > 3 or int(self.dict['texpert/ptxversion']) == 0:
                self.localChanges.append(makeChange(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+( (?!\\)[^\\\s]{{1,6}})) ([\S]{{1,{}}}\s*\n)", r"\1\u2000\5".format(self.dict['texpert/maxorphanlength']), flags=regex.M))
                self.localChanges.append(makeChange(r"(?<=\\[^ctm][^\\]+)(\s+[^ 0-9\\\n\u2000\u00A0]{{1,6}}) ((?:\p{{L}}\p{{M}}*|[^ 0-9\\\n\u2000]){{1,{}}}\n(?:\\[pmqsc]|$))".format(self.dict['texpert/maxorphanlength']), r"\1\u2000\2", flags=regex.S))
            else:
                self.localChanges.append(makeChange(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+( (?!\\)[^\\\s]{1,6})) ([\S]{1,9}\s*\n)", r"\1\u2000\5", flags=regex.M))
                self.localChanges.append(makeChange(r"(?<=\\[^ctm][^\\]+)(\s+[^ 0-9\\\n\u2000\u00A0]{1,6}) ([^ 0-9\\\n\u00A0\u2000]{1,8}\n(?:\\[pmqsc]|$))", r"\1\u2000\2", flags=regex.S))


        if self.asBool("document/preventwidows"):
            # Push the verse number onto the next line (using NBSP) if there is
            # a short widow word (3 characters or less) at the end of the line
            self.localChanges.append(makeChange(r"(\\v \d+([-,]\d+)? [\w]{1,3}) ", r"\1\u00A0", flags=regex.M)) 

        # By default, HIDE chapter numbers for all non-scripture (Peripheral) books (unless "Show... is checked)
        if not self.asBool("document/showxtrachapnums") and bk in nonScriptureBooks:
            self.localChanges.append(makeChange(r"(\\c \d+ ?\r?\n)", "", flags=regex.M))

        if self.asBool("document/glueredupwords"): # keep reduplicated words together
            self.localChanges.append(makeChange(r"(?<=[ ])(\w{3,}) \1(?=[\s,.!?])", r"\1\u2000\1", flags=regex.M)) 
        
        if self.asBool("notes/addcolon"): # Insert a colon between \fq (or \xq) and following \ft (or \xt)
            self.localChanges.append(makeChange(r"(\\[fx]q .+?):* ?(\\[fx]t)", r"\1: \2", flags=regex.M)) 

        # HELP NEEDED from MH to fix this section up again.
        # This may be good, but only when bumping the version number: r"(?<!\\\S+)\s(\p{Nd})", r"\u00A0\1"
        # in "\\r .+?[\r\n]+": "\s(\d)" > "~\1"  # Don't allow the line to break in the middle of a \r reference
        # Keep book number together with book name "1 Kings", "2 Samuel" within \xt and \xo # [\p{Nd}\p{L}])(\p{Nd})\s
        self.localChanges.append(makeChange(r"(?<![\p{Nd}\p{L}])(\p{Nd})\s(\p{L})", r"\1\u00A0\2", context=self.make_contextsfn(None, regex.compile(r"(\\(?:[xf]t|ref)\s[^\\]+)"))))
                        
        # Temporary fix to stop blowing up when \fp is found in notes (need a longer term TeX solution from DG or MH)
        # Solved on the TeX side on 11-Aug-2023, so we no longer need this hack below:
        # self.localChanges.append((None, regex.compile(r"\\fp ", flags=regex.M), r" --- ")) 
        
        if self.asBool("notes/keepbookwithrefs"): # keep Booknames and ch:vs nums together within \xt and \xo
            self.localChanges.append(makeChange(r"(\\p{Nd}?[^\s\p{Nd}\-\\,;]{3,}[^\\\s]*?)\s(\p{Nd}+[:.]\p{Nd}+(-\p{Nd}+)?)", r"\1\u2000\2", context=self.make_contextsfn(None, regex.compile(r"(\\(?:[xf]t|ref)\s[^\\|]+)"))))
            self.localChanges.append(makeChange(r"(\s\S) ", r"\1\u2000", context=self.make_contextsfn(None, regex.compile(r"(\\[xf]t\s[^\\]+)")))) # Ensure no floating single chars in note text
        
        # keep \xo & \fr refs with whatever follows (i.e the bookname or footnote) so it doesn't break at end of line
        self.localChanges.append(makeChange(r"(\\(xo|fr)\s+[^\\]+?)\s*\\", r"\1\u00A0\\"))

        for c in ("fn", "xr"):
            # Force all footnotes/x-refs to be either '+ ' or '- ' rather than '*/#'
            if self.asBool("notes/{}override".format(c)):
                t = "+" if self.asBool("notes/if{}autocallers".format(c)) else "-"
                self.localChanges.append(makeChange(r"\\{} ([^\\\s]+)".format(c[0]), r"\\{} {}".format(c[0],t)))
            # Remove the [spare] space after a note caller if the caller is omitted AND if after a digit (verse number).
            if self.asBool("notes/{}omitcaller".format(c)):
                self.localChanges.append(makeChange(r"(\d )(\\[{0}] - .*?\\[{0}]\*)\s+".format(c[0]), r"\1\2"))

        if self.asBool("notes/frverseonly"):
            self.localChanges.append(makeChange(r"\\fr \p{Nd}+[:.](\p{Nd}+)", r"\\fr \1"))

        if self.asBool("notes/xrverseonly"):
            self.localChanges.append(makeChange(r"\\xo \p{Nd}+[:.](\p{Nd}+)", r"\\xo \1"))

        # Paratext marks no-break space as a tilde ~, but the TeX handles it.
        # self.localChanges.append((None, regex.compile(r"~", flags=regex.M), r"\u00A0")) 

        # Paratext marks forced line breaks as //
        # self.localChanges.append((None, regex.compile(r"//", flags=regex.M), r"\u2028"))  

        # Convert hyphens from minus to hyphen
        if self.asBool("paragraph/ifnbhyphens"):
            self.localChanges.append(makeChange(r"(?<!\\(?:f|x|ef|fe)\s)((?<=\s)-|-(?=\s))", r"\u2011", flags=regex.M))
        # elif:
            # Is hyphenation turned on AND are there \u2010 in the hyphenation file?
            # self.localChanges.append(makeChange(r"(?<!\\(?:f|x|ef|fe)\s)((?<=\s)-|-(?=\s))", r"\u2010", flags=regex.M))
            

        # Capture \tc2-3 type spans
        def getspan(m):
            self.tablespans.add((m.group(1), m.group(2), m.group(3), m.group(4)))
            return m.group(0)
        self.localChanges.append(makeChange(r"\\(t[hc])([cr]?)(\d+)-(\d+)", getspan))
        # Wrap Hebrew and Greek words in appropriate markup to avoid tofu
        if self.asBool("project/autotaghebgrk"):
            if self.dict["document/script"][8:].lower() != "hebr":
                hchar = r"\p{sc=Hebr}\p{P}\p{sc=Zinh}\p{sc=Zyyy}--\\"  # Zyyy is common
                self.localChanges.append(makeChange(rf"(?<!\\[+]?wh[^\\]*)(\s+)([{hchar}][\\s{hchar}]*[\p{{sc=Hebr}}][\s{hchar}]*\b)", "\\1\\+wh \\2\\+wh*", flags=regex.M | regex.V1))
            if self.dict["document/script"][8:].lower() != "grek":
                gchar = r"\p{sc=Grek}\p{P}\p{sc=Zinh}\p{sc=Zyyy}--\\"
                self.localChanges.append(makeChange(rf"(?<!\\[+]?wg[^\\]*)(\s+)([{gchar}][\s{gchar}]*[\p{{sc=Grek}}][\s{gchar}]*\b)", "\\1\\+wg \\2\\+wg*", flags=regex.M | regex.V1))

        if self.asBool("document/toc") and self.asBool("document/multibook"):
            # Only do this IF the auto Table of Contents is enabled AND there is more than one book
            for c in range(1,4): # Remove any \toc lines that we don't want appearing in the ToC
                if not self.asBool("document/usetoc{}".format(c)):
                    self.localChanges.append(makeChange(r"(\\toc{} [^\n]+\n)".format(c), "", flags=regex.M | regex.S))

        # Add End of Book decoration PDF to Scripture books only if FancyBorders is enabled and .PDF defined
        if self.asBool("fancy/enableornaments") and self.asBool("fancy/endofbook") and bk not in nonScriptureBooks \
           and self.dict["fancy/endofbookpdf"].lower().endswith('.pdf'):
            self.localChanges.append(makeChange(r"\Z", r"\n", flags=regex.M))
        
        # Insert a rule between end of Introduction and start of body text (didn't work earlier, but might work now)
        # self.localChanges.append((None, regex.compile(r"(\\c\s1\s?\r?\n)", flags=regex.S), r"\\par\\vskip\\baselineskip\\hskip-\\columnshift\\hrule\\vskip 2\\baselineskip\n\1"))

        # Apply any changes specified in snippets
        for k, c in sorted(self._snippets.items(), key=lambda x: x[1][2].order):
            if self.printer is None:
                v = self.asBool(k) if c[1] is None else c[1](self.dict[k])
            elif c[1] is None:
                v = self.printer.get(c[0])
                self.dict[k] = "true" if v else "false"
            else:
                self.dict[k] = self.printer.get(c[0])
                v = c[1](self.dict[k])
            if v: # if the c_checkbox is true then extend the list with those changes
                if k == "snippets/fancyintro" and bk in nonScriptureBooks: # Only allow fancyIntros for scripture books
                    pass
                else:
                    self.localChanges.extend(c[2].regexes)

        ## Final tweaks
        # Strip out any spaces either side of an en-quad 
        self.localChanges.append(makeChange(r"(?<!\\\S+)\s?\u2000\s?", r"\u2000", flags=regex.M)) 
        # Change double-spaces to singles
        self.localChanges.append(makeChange(r" {2,}", r" ", flags=regex.M)) 
        # Remove any spaces before the \ior*
        self.localChanges.append(makeChange(r"\s+(?=\\ior\*)", r"", flags=regex.M)) 
        # Escape special codes % and $ that could be in the text itself
        self.localChanges.append(makeChange(r"(?<!\\\S*|\\[fx][^\\]*)([{}])(\s?)".format("".join(self._specialchars)), lambda m:"\\"+self._specialchars[m.group(1)]+("\\space{}".format(m.group(2)) if m.group(2) else " "), flags=regex.M))

        #self.localChanges.append((None, regex.compile(r"(?<=\n\r?)\r+"), ""))
        self.localChanges.append(makeChange(r"^\s*(?=\\id)", ""))

        # if self.printer is not None and self.printer.get("c_tracing"):
            # print("List of Local Changes:----------------------------------------------------------")
            # report = "\n".join("{}: {} -> {}".format(p[3], p[1].pattern, p[2]) for p in self.localChanges)
            # if getattr(printer, "logger", None) is not None:
                # printer.logger.insert_at_cursor(v)
            # else:
                # print(report)
        return self.localChanges

    def base(self, fpath):
        doti = fpath.rfind(".")
        return os.path.basename(fpath[:doti])

    def codeLower(self, fpath):
        cl = re.match(self.printer.getPicRe()+"$", self.base(fpath), re.I)
        if cl:
            return cl[0].lower()
        else:
            return ""

    def newBase(self, fpath):
        clwr = self.codeLower(fpath)
        if len(clwr):
            return clwr
        else:
            return re.sub('[()&+,.;: ]', '_', self.base(fpath).lower())

    def makeGlossaryFootnotes(self, printer, bk):
        # Glossary entries for the key terms appearing like footnotes
        prjid = printer.project.prjid
        prjdir = printer.project.path
        fname = printer.getBookFilename("GLO", prjid)
        infname = os.path.join(prjdir, fname)
        if os.path.exists(infname):
            with universalopen(infname, rewrite=True) as inf:
                dat = inf.read()
                # Note that this will only pick up the first para of glossary entries
                ge = re.findall(r"(\S+~\s*)?\\k (.+?)\\k\*(.+?)\r?\n", dat) # Finds all glossary entries in GLO book
                if ge is not None:
                    for g in ge:
                        gdefn = re.sub(r"\\xt (.+?)\\xt\*", r"\1", g[2])
                        gdefn = re.sub(r"\\w (.+?\|)?(.+?)\\w\*", r"\2", gdefn) # FIXME! This strips out \w from notes, preventing broken USFM (notes in notes). It would be better to leave them as-is, and avoid detecting them in notes, so readers can follow the chain.
                        gdefn = re.sub(r"\\", r"\\\\", gdefn)
                        gpfx = re.sub(r"~\s+"," ",g[0]) # Remove any trailing spaces from glossary item prefix
                        self.localChanges.append(makeChange(r"(\\w (.+?\|)?{} ?\\w\*)".format(g[1]), \
                                                                     r"\1\\f + {}\\fq {}: \\ft {}\\f* ".format(gpfx,g[1],gdefn), flags=regex.M))

    def filterGlossary(self, printer):
        # Only keep entries that have appeared in this collection of books
        def getk(e, attrib="lemma"):
            kval = e.get("lemma", None)
            if kval is None:
                kval = re.sub(r"[ \t]", "", e.text)
            return kval

        def addk(e, state):
            if e.tag != "char" or e.get("style", "") != "w":
                return
            kval = getk(e)
            if kval:
                self.found_glosses.add(kval.lower())        # case insensitive matching
            return state

        new_glosses = set()
        def capturek(e, state):
            if e.tag == "char" and e.get("style", "") == "k":
                nkval=getk(e, attrib="key").lower() 
                state = (nkval in self.found_glosses and nkval not in self.processed_glosses)
                if state:
                  self.processed_glosses.add(nkval)
                  logger.log(6,f"Checking active entry {nkval}")
            if state and e.tag == "char" and e.get("style", "") == "w":
                kval = getk(e)
                new_glosses.add(kval.lower())
                logger.log(6,f"found glossary entry {kval} in an active entry")
            return state

        self.found_glosses = set()
        self.printer.get_usfms()
        self.processed_glosses=set()
        for bk in printer.getBooks():
            if bk not in nonScriptureBooks:
                bkusfm = self.printer.usfms.get(bk)
                bkusfm.visitall(addk, bkusfm.getroot())
        count = self.dict.get("document/glossarydepth", 0) or 0
        logger.debug(f"Looking for chained glossary entries up to {count} deep")
        glousfm = self.printer.usfms.get("GLO")
      
        while count > 0 and glousfm is not None:
            glousfm.visitall(capturek, glousfm.getroot())
            logger.debug(f"Found glossary keys: {new_glosses}")
            self.found_glosses.update(new_glosses)
            new_glosses.clear()
            count -= 1
        logger.debug(f"Found glossary keys: {self.found_glosses}")

    def analyzeImageCopyrights(self):
        if self.dict['project/iffrontmatter'] == "":
            try:
                with open(self.printer.configFRT(), encoding="utf-8") as inf:
                    txt = inf.read()
            except FileNotFoundError:
                return
        else:
            txt = ""
        txt += self.dict.get('project/colophontext', '')
        for m in re.findall(r"(?i)\\(\S+).*?\\zimagecopyrights([A-Z]{2,3})?", txt):
            self.imageCopyrightLangs[m[1].lower() if m[1] else "en"] = m[0]
        return

    def generateEmptyImageCopyrights(self):
        self.analyzeImageCopyrights()
        res = [r"\def\zimagecopyrights{}"]
        for k in self.imageCopyrightLangs.keys():
            res.append(r"\def\zimagecopyrights{}{{}}".format(k))
        return "\n".join(res)

    def generateImageCopyrightText(self):
        self.printer.artpgs = {}
        mkr='pc'
        sensitive = self['document/sensitive']
        picpagesfile = os.path.join(self.docdir()[0], self['jobname'] + ".picpages")
        crdts = []
        cinfo = self.printer.copyrightInfo
        if cinfo is None or not len(cinfo):
            self.printer.readCopyrights()
            cinfo = self.printer.copyrightInfo
        self.analyzeImageCopyrights()
        if os.path.exists(picpagesfile):
            with universalopen(picpagesfile) as inf:
                dat = inf.read()

            # \figonpage{304}{56}{./tmpPics/cn01617.jpg}{tl}{© David C. Cook Publishing Co, 1978.}{x170.90504pt}
            rematch = r"(?i)\\figonpage\{(\d+)\}\{\d+\}\{(?:[^}]*\/)?(?:" + self.printer.getPicRe() + r"|(.*?))\.[^}]+\}\{.*?\}\{(.*?)?\}\{.+?\}"
            m = re.findall(rematch, dat)
            msngPgs = []
            customStmt = []
            if len(m):
                for f in m:
                    # print(f"{f[0]=} {f[1]=} {f[2]=} {f[3]=} {f[4]=} {f[5]=} ")
                    if not len(f) or not f[0] or f[5] == "None":
                        continue
                    a = 'co' if f[1] == 'cn' else f[1] # merge Cook's OT & NT illustrations together
                    if a == '' and f[5] != '':
                        p = f[5]
                    elif a == '':
                        p = "zz"
                        msngPgs += [f[0]] 
                    else:
                        p = a
                    self.printer.artpgs.setdefault(p, {}).setdefault(a,[]).append((int(f[0]),f[1]+f[2]))
            artistWithMost = ""
            if len(self.printer.artpgs):
                artpgcmp = [a for a in self.printer.artpgs if a != 'zz']
                if len(artpgcmp):
                    artistWithMost = max(artpgcmp, key=lambda x: len(self.printer.artpgs[x].values()))

        langs = set(self.imageCopyrightLangs.keys())
        langs.add("en")
        for lang in sorted(langs):
            crdtsstarted = False
            if os.path.exists(picpagesfile):
                hasOut = False
                mkr = self.imageCopyrightLangs.get(lang, "pc")
                rtl = lang in cinfo.get('rtl', [])
                if rtl == (self.dict['document/ifrtl'] == "false"):
                    mkr += "\\begin" + ("R" if rtl else "L")
                crdts.append("\\def\\zimagecopyrights{}{{%".format(lang.lower()))
                crdtsstarted = True
                plrls = cinfo.get('plurals', None)
                plstr = "" if plrls is None else plrls.get(lang, plrls["en"])
                cpytemplate = cinfo['templates']['imageCopyright'].get(lang,
                                        cinfo['templates']['imageCopyright']['en'])
                for art, pgs in self.printer.artpgs.items():
                    if art != artistWithMost and art != 'zz':
                        if len(pgs):
                            if art in "ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib".split("|"):
                                pages = [x[0] for x in pgs[art]]
                            else:
                                pages = [x[0] for x in pgs['']]
                            plurals = pluralstr(plstr, pages)
                            artinfo = cinfo["copyrights"].get(art.lower(), {'copyright': {'en': art}, 'sensitive': {'en': art}})
                            if artinfo is not None and (art in cinfo['copyrights'] or len(art) > 5):
                                artstr = artinfo["copyright"].get(lang, artinfo["copyright"]["en"])
                                if sensitive and "sensitive" in artinfo:
                                    artstr = artinfo["sensitive"].get(lang, artinfo["sensitive"]["en"])
                                cpystr = multstr(cpytemplate, lang, len(pages), plurals, artstr.replace("_", "\u00A0"))
                                crdts.append("\\{} {}".format(mkr, cpystr))
                            else:
                                crdts.append(_("\\message{{Warning: No copyright statement found for: {} on pages {}}}")\
                                                .format(art, plurals))
                            hasOut = True
                if len(msngPgs):
                    plurals = pluralstr(plstr, msngPgs)
                    template = cinfo['templates']['imageExceptions'].get(lang,
                                        cinfo['templates']['imageExceptions']['en'])
                    exceptPgs = " " + multstr(template, lang, len(msngPgs), plurals)
                else:
                    exceptPgs = ""

                if len(artistWithMost):
                    artinfo = cinfo["copyrights"].get(artistWithMost, 
                                {'copyright': {'en': artistWithMost}, 'sensitive': {'en': artistWithMost}})
                    if artinfo is not None and (artistWithMost in cinfo["copyrights"] or len(artistWithMost) > 5):
                        # print(f"{art=} {artistWithMost=} {self.printer.artpgs=}")
                        if artistWithMost in "ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib".split("|"):
                            pages = [x[0] for x in self.printer.artpgs[artistWithMost][artistWithMost]]
                        else:
                            pages = [x[0] for x in self.printer.artpgs[artistWithMost]['']]
                        plurals = pluralstr(plstr, pages)
                        artstr = artinfo["copyright"].get(lang, artinfo["copyright"]["en"])
                        if sensitive and "sensitive" in artinfo:
                            artstr = artinfo["sensitive"].get(lang, artinfo["sensitive"]["en"])
                        if not hasOut:
                            template = cinfo['templates']['allIllustrations'].get(lang,
                                cinfo['templates']['allIllustrations']['en'])
                        else:
                            template = cinfo['templates']['exceptIllustrations'].get(lang,
                                cinfo['templates']['exceptIllustrations']['en'])
                        cpystr = template.format(artstr.replace("_", "\u00A0"), exceptPgs)
                        crdts.append("\\{} {}".format(mkr, cpystr))
            if self.dict['notes/ifxrexternalist']:
                if self.dict['notes/xrlistsource'] == "standard":
                    msg = "\\{} {}".format(mkr, cinfo['templates']['openbible.info'].get(lang,
                                cinfo['templates']['openbible.info']['en']).replace("_", "\u00A0"))
                else:
                    msg = getattr(self, 'xrefcopyright', None)
                if msg is not None:
                    if not crdtsstarted:
                        crdts.append("\\def\\zimagecopyrights{}{{%".format(lang.lower()))
                        crdtsstarted = True
                    crdts.append(msg)
            if crdtsstarted:
                crdts.append("}")
        if len(crdts):
            crdts.append("\\let\\zimagecopyrights=\\zimagecopyrightsen")
        return "\n".join(crdts) + ("\n" if len(crdts) else "")

    def createXrefTriggers(self, bk, prjdir, triggers):
        if self.xrefs is None:
            cfilter = self.dict['notes/xrfilterbooks']
            if cfilter == "pub":
                bl = self.printer.get("ecb_booklist", "").split()
                filters = set(bl)
            elif cfilter == "prj":
                filters = set(self.printer.getAllBooks().keys())
            elif cfilter == "all":
                filters = None
            elif cfilter == "ot":
                filters = allbooks[:39]
            elif cfilter == "nt":
                filters = allbooks[40:67]
            if filters is not None and len(filters) == 0:
                filters = None
            localfile = None
            xrsrc = self.dict['notes/xrlistsource']
            if xrsrc == "strongs_proj":
                localfile = os.path.join(self.printer.project.path, "TermRenderings.xml")
                if not os.path.exists(localfile):
                    localfile = None
            if xrsrc[-1] in "0123456789":
                listsize = int(xrsrc[-1])
                xrsrc = xrsrc[:-2]
            else:
                listsize = 0
            logger.debug(f"Create Xrefs: {bk=} {xrsrc=}, {localfile=}")
            # import pdb; pdb.set_trace()
            self.xrefs = Xrefs(self, filters, prjdir,
                    self.dict['project/selectxrfile'] if self.dict['notes/xrlistsource'] == 'custom' else None,
                    listsize, xrsrc, localfile, self.dict['strongsndx/shownums'], self.dict['notes/xrverseonly'])
        return self.xrefs.process(bk, triggers, usfm=self.printer.get_usfm(bk))

