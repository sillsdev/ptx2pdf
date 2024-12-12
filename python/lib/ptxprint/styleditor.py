
import re, os
from ptxprint.usfmutils import Sheets
from ptxprint.sfm.style import Marker
from ptxprint.font import FontRef
from ptxprint.utils import f2s, textocol, coltotex, coltoonemax, Path, saferelpath, asfloat
from copy import deepcopy
import logging

logger = logging.getLogger(__name__)

class _CEnum:
    def __init__(self, *vals):
        self.vals = vals

    def __contains__(self, v):
        return v.lower() in self.vals

    def __str__(self):
        return "in " + ", ".join(self.vals)

class _CRange:
    def __init__(self, first, last=None):
        if last is None:
            last = first
            first = 0.
        self.first = first
        self.last = last

    def __contains__(self, v):
        v = asfloat(v, None)
        if v is None:
            return False
        if v < self.first:
            return False
        if self.last is not None and v > self.last:
            return False
        return True

    def __str__(self):
        return "in range({}, {})".format(self.first, self.last)

class _CValue:
    def __init__(self, val):
        self.value = val

    def __contains__(self, v):
        v = asfloat(v, None)
        if v is None:
            return False
        return v == self.value

    def __str__(self):
        return "== {}".format(self.value)

class _CNot:
    def __init__(self, constraint):
        self.constraint = constraint

    def __contains__(self, v):
        return not v in self.constraint

    def __str__(self):
        return "not(" + str(self.constraint) + ")"

constraints = {
    'texttype': _CEnum('versetext', 'notetext', 'bodytext', 'title', 'section', 'other',
                        'chapternumber', 'versenumber', 'unspecified', 'standalone'),
    'styletype': _CEnum('paragraph', 'character', 'note', 'milestone', 'standalone', ''),
    'fontsize': _CRange(2.),
    'fontscale': _CRange(2.),
    'raise': _CNot(_CValue(0.)),
    'linespacing': _CRange(0.01, 2.5),
}

mkrexceptions = {k.lower().title(): k for k in ('BaseLine', 'TextType', 'TextProperties', 'FontName',
                'FontSize', 'FirstLineIndent', 'LeftMargin', 'RightMargin',
                'SpaceBefore', 'SpaceAfter', 'CallerStyle', 'CallerRaise',
                'NoteCallerStyle', 'NoteCallerRaise', 'NoteBlendInto', 'LineSpacing', 'UnderChar',
                'StyleType', 'ColorName', 'XMLTag', 'TEStyleName', 'ztexFontFeatures', 'ztexFontGrSpace',
                'FgImage', 'FgImagePos', 'FgImageScale', 'FgImageScaleTo', 
                'BgImage', 'BgImagePos', 'BgImageScale', 'BgImageScaleTo', 'BgImageLow',
                'BgImageColour', 'BgImageColor', 'BgImageAlpha', 'BgImageOversize', 'BgColour', 'BgColor',
                'BorderWidth', 'BorderLineWidth', 
                'BorderColour', 'BorderColor', 'BorderFillColour', 'BorderFillColor',
                'BorderPadding', 'BorderVPadding', 'BorderHPadding', 
                'BorderTPadding', 'BorderBPadding', 'BorderLPadding', 'BorderRPadding', 
                'BoxPadding', 'BoxTPadding', 'BoxBPadding', 'BoxLPadding', 'BoxRPadding', 
                'BorderPaddingInnerOuter','BoxPaddingInnerOuter',
                'BoxVPadding', 'BoxHPadding', 'BorderStyle', 'BorderStyleExtra', 'BorderRef', 'NonJustifiedFill',
                'SidebarGridding','SpaceBeside', 'VerticalAlign',
                'BorderPatternLeft','BorderPatternRight', 'BorderPatternTop','BorderPatternBot','OrnamentScaleRef')}
binarymkrs = {"bold", "italic", "smallcaps"}

absolutes = {"baseline", "raise", "callerraise", "notecallerraise"}
aliases = {"q", "s", "mt", "to", "imt", "imte", "io", "iq", "is", "ili", "pi",
           "qm", "sd", "ms", "mt", "mte", "li", "lim", "liv", }
_defFields = {"Marker", "EndMarker", "Name", "Description", "OccursUnder", "TextProperties", "TextType", "StyleType"}

def asFloatPts(self, s, mrk=None, model=None):
    if mrk is None:
        mrk = self.marker
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*(\D*?)\s*$", str(s))
    if m:
        try:
            v = float(m[1])
        except (TypeError, ValueError):
            v = 0.
        units = m[2]
        if units == "" or units.lower() == "pt" or mrk is None:
            return v
        elif units == "in":
            return v * 72.27
        elif units == "mm":
            return v * 72.27 / 25.4
        try:
            fsize = float(self.getval(mrk, "FontSize"))
        except TypeError:
            return v
        if fsize is None:
            return v
        try:
            bfsize = float(self.model.get("s_fontsize"))
        except TypeError:
            return v
        if units == "ex":
            return v * fsize / 12. / 2.
        elif units == "em":
            return v * fsize / 12.
        return v
    else:
        try:
            return float(s)
        except (ValueError, TypeError):
            return 0.

def toFloatPts(self, v, mrk=None, model=None, parm=None):
    return "{} pt".format(f2s(float(v)))

def fromFloat(self, s, mrk=None, model=None):
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.

def toFloat(self, v, mrk=None, model=None, parm=None):
    return f2s(float(v))

def from12(self, s, mrk=None, model=None):
    try:
        return float(s) / 12.
    except (TypeError, ValueError):
        return 0.

def to12(self, v, mrk=None, model=None, parm=None):
    return f2s(float(v) * 12.)

def fromBool(self, s, mrk=None, model=None):
    return not(s is None or s is False or s == "-")

def toBool(self, v, mrk=None, model=None, parm=None):
    return "" if v else "-"

def fromSet(self, s, mrk=None, model=None):
    if isinstance(s, dict):
        return s
    elif isinstance(s, str):
        return {k:v for v,k in enumerate(s.split())}
    else:
        return {k:v for v,k in enumerate(s)}

def toSet(self, s, mrk=None, model=None, parm=None):
    if isinstance(s, str):
        return s
    elif isinstance(s, dict):
        return " ".join(k for k,v in sorted(s.items(), key=lambda x:x[1]))
    else:
        return " ".join(s)

def fromFont(self, s, mrk=None, model=None):
    if mrk is None:
        mrk = self.marker
    class Shim:
        def get(subself, key, default=None):
            if key == 'FontName':
                return self.sheet.get(mrk, {}).get(key,
                        self.basesheet.get(mrk, {}).get(key, default))
            return self.getval(mrk, key, default)
    return FontRef.fromTeXStyle(Shim())

def toFont(self, v, mrk=None, model=None, parm=None):
    if v is None:
        return
    if mrk is None:
        mrk = self.marker
    class Shim:
        def __setitem__(subself, key, val):
            if key == 'FontName':
                if mrk not in self.sheet:
                    self.sheet[mrk] = Marker()
                self.sheet[mrk][key] = val
            else:
                self.setval(mrk, key, val)
        def __contains__(subself, key):
            return self.haskey(mrk, key)
        def __delitem__(subself, key):
            return self.sheet.get(mrk, {}).pop(key, None)
        def __getitem__(subself, key):
            return self.sheet.get(mrk, {}).get(key, None)
        def pop(subself, key, dflt):
            return self.sheet.get(mrk, {}).pop(key, dflt)
    regularfont = model.get("bl_fontR")
    oldfont = self.basesheet.get(mrk, {}).get("font", None)
    return v.updateTeXStyle(Shim(), regular=regularfont, force=oldfont is not None, noStyles=(parm is not None))

def fromOneMax(self, v, mrk=None, model=None):
    res = coltotex(textocol(v))
    return res

def toOneMax(self, v, mrk=None, model=None, parm=None):
    res = " ".join("{:.2f}".format(x) for x in coltoonemax(textocol(v)))
    return res

def fromFileName(self, s, mrk=None, model=None):
    v = re.sub(r"\\ ", " ", s)
    return v.strip('"')

def toFileName(self, s, mrk=None, model=None, parm=None):
    v = s.replace("\\", "/") # .replace(" ", "\\ ")
    if v is not None and not v.startswith('"') and len(v):
        return '"'+v+'"'
    return v

# [2] is unused
_fieldmap = {
    'bold':             (fromBool, toBool, None),
    'italic':           (fromBool, toBool, None),
    'superscript':      (fromBool, toBool, None),
    'smallcaps':        (fromBool, toBool, None),
    'firstlineindent':  (fromFloat, toFloat, 0.),
    'leftmargin':       (fromFloat, toFloat, 0.),
    'rightmargin':      (fromFloat, toFloat, 0.),
    'nonjustifiedfill': (fromFloat, toFloat, 0.25),
    'linespacing':      (fromFloat, toFloat, 1.),
    'raise':            (asFloatPts, toFloatPts, 0.),
    'baseline':         (asFloatPts, toFloatPts, None),
    'callerraise':      (asFloatPts, toFloatPts, None),
    'notecallerraise':  (asFloatPts, toFloatPts, None),
    'fontsize':         (from12, to12, 12.),
    'spacebefore':      (from12, to12, 0),
    'spaceafter':       (from12, to12, 0),
    'font':             (fromFont, toFont, None),
    'textproperties':   (fromSet, toSet, None),
    'occursunder':      (fromSet, toSet, None),
    'bordercolor':      (fromOneMax, toOneMax, None),
    'borderfillcolor':  (fromOneMax, toOneMax, None),
    'bgimagecolor':     (fromOneMax, toOneMax, None),
    'bgcolor':          (fromOneMax, toOneMax, None),
    'bgimage':          (fromFileName, toFileName, None),
    'fgimage':          (fromFileName, toFileName, None)
}

class StyleEditor:

    def __init__(self, model, basepath=None):
        self.model = model
        self.sheet = {}
        self.marker = None
        self.registers = {}
        self.reset(basepath=basepath)

    def copy(self):
        res = self.__class__(self.model)
        res.sheet = Sheets(base=self.sheet)
        res.basesheet = Sheets(base=self.basesheet)
        res.marker = self.marker
        res.registers = dict(self.registers)
        return res

    def reset(self, basepath=None):
        if basepath is None:
            self.basesheet = {}
        else:
            self.basesheet = self._read_styfile(basepath)

    def _read_styfh(self, fh):
        fieldre = re.compile(r"^\s*\\(\S+)\s*(.*?)\s*$")
        res = {}
        curr = {}
        for l in fh.readlines():
            m = fieldre.match(l)
            if m:
                mk = m.group(1)
                v = m.group(2)
                if mk.lower() == "fontname":
                    mk = "font"
                if mk.lower() == "marker":
                    curr = {}
                    res[v] = curr
                    mrk = v
                    continue
                elif mk.lower() in _fieldmap:
                    v = _fieldmap[mk.lower()][0](self, v, mrk=mrk, model=self.model)
                curr[mk.lower()] = v
        return res

    def _read_styfile(self, fname):
        if not os.path.exists(fname):
            return {}
        logger.debug(f"Reading {fname}") 
        with open(fname, encoding="utf-8") as inf:
            res = self._read_styfh(inf)
        return res

    def allStyles(self):
        res = set(self.basesheet.keys())
        res.update(self.sheet.keys())
        return res

    def allValueKeys(self, m):
        res = set(list(self.basesheet.get(m, {}).keys()))
        res.update(list(self.sheet.get(m, {}).keys()))
        return res

    def asStyle(self, m):
        if m is None:
            res = {}
            for m in self.allStyles():
                res[m] = {k:v for k, v in self.basesheet.get(m, {}).items()}
                res[m].update({k:v for k, v in self.sheet.get(m, {}).items()})
        else:
            res = {k:v for k, v in self.basesheet.get(m, {}).items()}
            res.update({k:v for k, v in self.sheet.get(m, {}).items()})
        return res

    def getval(self, mrk, key, default=None, baseonly=False):
        if mrk not in self.sheet:
            return default
        res = self.sheet[mrk].get(key.lower(), None) if not baseonly else None
        if res is None or (mrk in _defFields and not len(res)):
            res = self.basesheet[mrk].get(key.lower(), default) if mrk in self.basesheet else default
        return res

    def setval(self, mrk, key, val, ifunchanged=False, parm=None, mapin=False):
        if ifunchanged and (self.basesheet[mrk].get(key.lower(), None) if mrk in self.basesheet else None) != \
                (self.sheet[mrk].get(key.lower(), None) if mrk in self.sheet else None):
            return
        if mapin and key.lower() in _fieldmap and val is not None:
            val = _fieldmap[key.lower()][0](self, val, mrk=mrk, model=self.model)
        # 'fixing' this to default to "" causes problems with things like \Italic where nothing is True
        oldval = self.basesheet[mrk].get(key.lower(), None) if mrk in self.basesheet else None
        if mrk in self.sheet and key in self.sheet[mrk] and (val is None or val == oldval):
            del self.sheet[mrk][key.lower()]
        elif oldval != val and val is not None:
            if mrk not in self.sheet:
                self.sheet[mrk] = {}
            self.sheet[mrk][key.lower()] = val
            self.model.changed()
        # do we really want to do this?
        elif key in self.basesheet.get(mrk, {}) and val is None:
            del self.basesheet[mrk][key.lower()]
            self.model.changed()

    def haskey(self, mrk, key):
        if key in self.sheet.get(mrk, {}) or key.lower() in self.basesheet.get(mrk, {}):
            return True
        return False

    def addMarker(self, mrk, name):
        self.sheet[mrk] = Marker({" deletable": True, "name": name})

    def get_font(self, mrk, style=""):
        f = self.getval(mrk, " font")
        if f is not None:
            return f
        f = self.model.getFont(style if len(style) else "regular")
        return f

    def _merge(self, sheet, styles):
        for k, v in styles.items():
            if k in sheet:
                sheet[k].update(v)
            else:
                sheet[k] = v
        return sheet

    def load(self, sheetfiles):
        if len(sheetfiles) == 0:
            return
        foundp = False
        for s in sheetfiles[:-1]:
            logger.debug(f"loading stylesheet: {s}")
            sheet = self._read_styfile(s)
            self._merge(self.basesheet, sheet)
        self.test_constraints(self.basesheet)
        self.sheet = self._read_styfile(sheetfiles[-1])
        self.test_constraints(self.sheet)

    def loadfh(self, fh):
        self.sheet = self._read_styfh(fh)

    def test_constraints(self, sheet):
        for m, s in sheet.items():
            for k, v in list(s.items()):
                c = constraints.get(k.lower(), None)
                if c is not None and not v in c:
                    logger.info(f"Failed constraint: {m}/{k} = {v} constraint: {c}")
                    del s[k]

    def _convertabs(self, key, val):
        baseline = float(self.model.get("s_linespacing", 1.))
        if key.lower() == "baseline":
            return val * baseline
        elif key.lower() == "linespacing":
            return val / baseline
        return val

    def _eq_val(self, a, b, key=""):
        if (b is None) ^ (a is None):
            return False
        elif key.lower() in absolutes:
            fa = asFloatPts(self, str(a))
            fb = asFloatPts(self, str(b))
            return fa == fb
        elif isinstance(a, dict) and isinstance(b, dict):
            return set(a.keys()) == set(b.keys())
        else:
            try:
                fa = float(a)
                fb = float(b)
                return abs(fa - fb) < 0.005
            except (ValueError, TypeError):
                pass
            if key.lower() not in binarymkrs:
                a = a or ""
                b = b or ""
            return a == b

    def _str_val(self, v, key="", mrk=None):
        if key in _fieldmap:
            v = _fieldmap[key][1](self, v, mrk, model=self.model, parm=None)
        if isinstance(v, (set, list)):
            logger.debug(f"StyleEditor:_str_val found {type(v)} for {mrk}/{key}")
            res = " ".join(self._str_val(x, key, mrk) for x in sorted(v))
        elif isinstance(v, float):
            res = f2s(v)
        else:
            res = str(v)
        return res

    def output_diffile(self, outfh, inArchive=False, sheet=None, basesheet=None):
        def normmkr(s):
            x = s.lower().title()
            return mkrexceptions.get(x, x)
        if basesheet is None:
            basesheet = self.basesheet
        if sheet is None:
            sheet = self.sheet
        for m in sorted(self.allStyles()):
            markerout = False
            if m in aliases:
                sm = self.asStyle(m+"1")
            elif inArchive:
                sm = sheet.get(m, {}).copy()
            else:
                sm = sheet.get(m, {})
            om = basesheet.get(m, {})
            if 'zderived' in om or 'zderived' in sm:
                continue
            if 'font' in sm:
                v = _fieldmap['font'][1](self, sm['font'], m, model=self.model, parm=None)
            for k, v in sm.items():
                if k.startswith(" ") or k == "font":
                    continue
                if k == "name":
                    v = self.getval(m, k, v)
                other = om.get(k, None)
                if not self._eq_val(other, v, key=k):
                    if not markerout:
                        outfh.write("\n\\Marker {}\n".format(m))
                        markerout = True
                    outfh.write("\\{} {}\n".format(normmkr(k), self._str_val(v, k, m)))

    def merge(self, basese, newse):
        for m in newse.sheet.keys():
            allkeys = newse.allValueKeys(m)
            allkeys.update(basese.allValueKeys(m))
            allkeys.update(self.allValueKeys(m))
            for k in allkeys:
                nv = newse.getval(m, k)
                bv = basese.getval(m, k)
                sv = self.getval(m, k)
                if sv != bv:
                    continue
                if nv != bv:
                    self.setval(m, k, nv)

    def mergein(self, newse, force=False, exclfields=None):
        allstyles = self.allStyles()
        for m in newse.sheet.keys():
            if m not in allstyles:
                self.addMarker(str(m), str(newse.getval(m, 'name', "")))
            allkeys = newse.allValueKeys(m) | self.allValueKeys(m)
            for k in allkeys:
                if exclfields is not None and k in exclfields:
                    continue
                nv = newse.getval(m, k)
                bv = self.getval(m, k, baseonly=True)
                sv = self.getval(m, k)
                if not force and sv != bv:
                    continue
                if force or nv != bv and nv is not None:
                    self.setval(m, k, nv)
