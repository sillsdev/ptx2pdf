
import re
from ptxprint.usfmutils import Sheets
from copy import deepcopy

mkrexceptions = {k.lower().title(): k for k in ('BaseLine', 'TextType', 'TextProperties', 'FontName',
                'FontSize', 'FirstLineIndent', 'LeftMargin', 'RightMargin',
                'SpaceBefore', 'SpaceAfter', 'CallerStyle', 'CallerRaise',
                'NoteCallerStyle', 'NoteCallerRaise', 'NoteBlendInto', 'LineSpacing',
                'StyleType', 'ColorName', 'XMLTag', 'TEStyleName')}

absolutes = {"baseline", "raise", "callerraise", "notecallerraise"}

class StyleEditor:

    def __init__(self, model):
        self.model = model
        self.sheet = None
        self.basesheet = None
        self.marker = None
        self.registers = {}

    def allStyles(self):
        if self.sheet is None:
            return {}
        res = set(self.basesheet.keys())
        res.update(self.sheet.keys())
        return res

    def getval(self, mrk, key):
        if self.sheet is None:
            raise KeyError(f"{mrk} + {key}")
        return self.sheet.get(mrk, {}).get(key, self.basesheet.get(mrk, {}).get(key, None))

    def setval(self, mrk, key, val, ifunchanged=False):
        if self.sheet is None:
            raise KeyError(f"{mrk} + {key}")
        if ifunchanged and self.basesheet.get(mrk, {}).get(key, None) != \
                self.sheet.get(mrk, {}).get(key, None):
            return
        if val is None and key in self.sheet.get(mrk, {}):
            del self.sheet[mrk][key]
            return
        if self.basesheet.get(mrk, {}).get(key, None) != val:
            self.sheet.setdefault(mrk, {})[key] = val

    def registerFn(self, mark, key, fn):
        self.registers.setdefault(mark, {})[key.lower()] = fn

    def load(self, sheetfiles):
        if len(sheetfiles) == 0:
            return
        foundp = False
        self.basesheet = Sheets(sheetfiles[:-1])
        self.sheet = Sheets(sheetfiles[-1:], base=self.basesheet)

    def _convertabs(self, key, valstr):
        def asfloat(v, d):
            try:
                return float(v)
            except (ValueError, TypeError):
                return d
        basesize = float(self.model.get("s_fontsize", 12.))
        baseline = float(self.model.get("s_linespacing", 14.))
        if key.lower() == "fontsize":
            res = asfloat(valstr, 1.) * basesize
        elif key.lower() == "baseline":
            res = asfloat(valstr, 12.) * baseline / 12.
        elif key.lower() == "fontscale": 
            res = asfloat(valstr, basesize) / basesize
        elif key.lower() == "linespacing":
            res = asfloat(valstr, baseline) / baseline * 12.
        return res

    def _setData(self, key, val):
        if self.basesheet.get(self.marker, {}).get(key, None) != val:
            self.sheet[self.marker][key] = val
            fn = self.registers.get(self.marker, {}).get(key.lower(), None)
            if fn is not None:
                fn(key, val)

    def _eq_val(self, a, b, key=""):
        if key.lower() in absolutes:
            fa = self.asFloatPts(str(a))
            fb = self.asFloatPts(str(b))
        else:
            try:
                fa = float(a)
                fb = float(b)
            except (ValueError, TypeError):
                return b is None if a is None else (False if b is None else a == b)
        return abs(fa - fb) < 0.005

    def _str_val(self, v, key=""):
        if isinstance(v, (set, list)):
            if key.lower() == "textproperties":
                res = " ".join(x.lower().title() if x else "" for x in sorted(v))
            else:
                res = " ".join(self._str_val(x, key) for x in v)
        elif key.lower() in absolutes:
            fv = self.asFloatPts(str(v))
            res = "{:.3f} pt".format(fv)
        elif isinstance(v, float):
            res = re.sub(r"(:\.0)?0$", "", str(int(v * 100) / 100.))
        else:
            res = str(v)
        if key.lower() == "baseline":
            res = re.sub(r"^\s*(.*\d+)\s*$", r"\1pt", res)
        return res

    def output_diffile(self, outfh):
        def normmkr(s):
            x = s.lower().title()
            return mkrexceptions.get(x, x)
        for m in self.allStyles():
            markerout = False
            sm = self.sheet.get(m, {})
            om = self.basesheet.get(m, {})
            for k,v in sm.items():
                if k.startswith(" "):
                    continue
                other = om.get(k, None)
                if not self._eq_val(other, v, key=k):
                    if not markerout:
                        outfh.write("\n\\Marker {}\n".format(m))
                        markerout = True
                    outfh.write("\\{} {}\n".format(normmkr(k), self._str_val(v, k)))

    def asFloatPts(self, s, mrk=None):
        if mrk is None:
            mrk = self.marker
        m = re.match(r"^\s*(-?\d+(?:\.\d*))\s*(\D*?)\s*$", s)
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

