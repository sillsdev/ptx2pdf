
import re
from ptxprint.usfmutils import Sheets
from ptxprint.sfm.style import Marker, CaselessStr
from copy import deepcopy

mkrexceptions = {k.lower().title(): k for k in ('BaseLine', 'TextType', 'TextProperties', 'FontName',
                'FontSize', 'FirstLineIndent', 'LeftMargin', 'RightMargin',
                'SpaceBefore', 'SpaceAfter', 'CallerStyle', 'CallerRaise',
                'NoteCallerStyle', 'NoteCallerRaise', 'NoteBlendInto', 'LineSpacing',
                'StyleType', 'ColorName', 'XMLTag', 'TEStyleName')}

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
                self.sheet.get(self.marker, {}).get(key, None):
            return
        if val is None and key in self.sheet.get(mrk, {}):
            del self.sheet[mrk][key]
            return
        if self.basesheet.get(mrk, {}).get(key, None) != val:
            self.sheet.setdefault(self.marker, {})[key] = val

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
            except TypeError:
                return d
        if key == "FontSize":
            basesize = float(self.get("s_fontsize", 12.))
            res = asfloat(valstr, 1.) * basesize
        elif key == "FontScale":
            basesize = float(self.get("s_fontsize", 12.))
            res = asfloat(valstr, basesize) / basesize
        elif key == "LineSpacing":
            linespacing = float(self.get("s_linespacing", 12.))
            res = asfloat(valstr, linespacing) / linespacing
        elif key == "BaseLine":
            linespacing = float(self.get("s_linespacing", 12.))
            res = asfloat(valstr, 1.) * linespacing
        return res

    def _setData(self, key, val):
        if self.basesheet.get(self.marker, {}).get(key, None) != val:
            self.sheet[self.marker][key] = val
            fn = self.registers.get(self.marker, {}).get(key.lower(), None)
            if fn is not None:
                fn(key, val)

    def _eq_val(self, a, b):
        try:
            fa = float(a)
            fb = float(b)
            return abs(fa - fb) < 0.005
        except (ValueError, TypeError):
            return b is None if a is None else (False if b is None else a == b)

    def _str_val(self, v, key=""):
        if isinstance(v, (set, list)):
            if key.lower() == "textproperties":
                res = " ".join(x.lower().title() if x else "" for x in sorted(v))
            else:
                res = " ".join(self._str_val(x, key) for x in v)
        elif isinstance(v, float):
            res = re.sub(r"(:\.0)?0$", "", str(int(v * 100) / 100.))
        else:
            res = str(v)
        if key.lower() == "baseline":
            res = re.match(r"^\s*(.*\d+)\s*$", r"\1pt", str(res))
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
                if not self._eq_val(other, v):
                    if not markerout:
                        outfh.write("\n\\Marker {}\n".format(m))
                        markerout = True
                    outfh.write("\\{} {}\n".format(normmkr(k), self._str_val(v, k)))


