from ptxprint.utils import f2s

# 'code', 'pg', 'prj', 'cfg', 'captions', 'width', 'color', 'prjguid'
# poly/k: (attr, type)
configmap = { 
    "projectid":    ("prj", str),
    "projectguid":  ("prjguid", str),
    "config":       ("cfg", str),
    "page":         ("pg", str),
    "fraction":     ("width", float),
    "captions":     ("captions", bool),
    "backcolor":    ("color", str)
}

def updateTMfromView(texmodel, view):
    for k, v in configmap.items():
        val = view.get(f"poly{k}_", "")
        # print(f"{k}={val}")
        texmodel.dict[f"poly/{k}"] = val 

class PolyglotConfig:
    def __init__(self):
        self.prj = None
        self.prjguid = None
        self.cfg = None
        self.pg = None
        self.width = None
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
                val = (val or 0) / 100
            view.set(f"poly{k}_", str(val), skipmissing=True)
            
