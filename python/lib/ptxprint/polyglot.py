from ptxprint.utils import f2s

configmap = {
    "projectid":    ("prjid", str),
    "projectguid":  ("prjguid", str),
    "config":       ("cfgid", str),
    "page":         ("page", int),
    "fraction":     ("fraction", float),
    "captions":     ("captions", bool),
    "backcolor":    ("backcolor", str)
}

class PolyglotConfig:
    def __init__(self):
        self.prjid = None
        self.prjguid = None
        self.cfgid = None
        self.fraction = None
        self.captions = None
        self.backcolor = None

    def readConfig(self, config, sect):
        for k, v in configmap.items():
            print(f"{k=} {v=}")
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
