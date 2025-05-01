from ptxprint.utils import f2s
from ptxprint.modelmap import ModelMap

# 'code', 'pg', 'prj', 'cfg', 'captions', 'fraction', 'fontsize', 'baseline', 'weight', 'color', 'prjguid'
# poly/k: (attr, type)
configmap = { 
    "code":         ("code", str, None),
    "projectid":    ("prj", str, None),
    "projectguid":  ("prjguid", str, None),
    "config":       ("cfg", str, None),
    "page":         ("pg", str, None),
    "fraction":     ("fraction", float, ["poly/fraction"]),
    "weight":       ("weight", float, None),
    "fontsize":     ("fontsize", float, ["paper/fontfactor"]),
    "baseline":     ("baseline", float, ["paragraph/linespacing"]),
    "captions":     ("captions", bool, ["document/iffigshowcaptions"]),
    "backcolor":    ("color", str, ["document/diglotcolour", "document/ifdiglotcolour"])
}

class PolyglotConfig:
    def __init__(self):
        self.code = None
        self.prj = None
        self.prjguid = None
        self.cfg = None
        self.pg = None
        self.fraction = None
        self.weight = None
        self.fontsize = None
        self.baseline = None
        self.captions = None
        self.color = None
        
    def __repr__(self):
        return "polyglot config (" + ", ".join(str(getattr(self, a[0], "None")) for a in configmap.values()) + ")"

    def readConfig(self, config, sect):
        for k, v in configmap.items():
            nv = None
            if v[1] == float:
                nv = config.getfloat(sect, k, fallback=None)
            if v[1] == int:
                nv = int(config.get(sect, k, fallback=1))
            elif v[1] == str:
                nv = config.get(sect, k, fallback=None)
            elif v[1] == bool:
                nv = config.get(sect, k, fallback="false").strip().lower() in ("true", "1", "yes", "on")
            if nv is not None:
                setattr(self, v[0], nv)

    def writeConfig(self, config, sect):
        for k, v in configmap.items():
            nv = getattr(self, v[0])
            if nv is None:
                continue
            if v[1] == float:
                nv = f2s(nv)
            if v[1] == int:
                nv = str(nv)
            elif v[1] == bool:
                nv = "true" if nv else "false"
            if not config.has_section(sect):
                config.add_section(sect)
            config.set(sect, k, nv)

    def updateView(self, view):
        for k, v in configmap.items():
            val = getattr(self, v[0], "")
            if k == "fraction":
                val = (val or 0)
            view.set(f"poly{k}_", str(val), skipmissing=True)
            
    def updateTM(self, texmodel):
        for k, v in configmap.items():
            if v[2] is None:
                continue
            val = getattr(self, v[0], "")
            for t in v[2]:
                fn = ModelMap.get(t, None)
                if fn is not None:
                    fn = fn.process
                texmodel.dict[t] = fn(None, val) if fn is not None else val
        