
configmap = {
    "projectid":    ("prjid", str),
    "projectguid":  ("prjguid", str),
    "config":       ("cfgid", str),
    "fraction":     ("fraction", float)
}

class PolyglotConfig:
    def __init__(self):
        self.prjid = None
        self.prjguid = None
        self.cfgid = None
        self.fraction = None

    def readConfig(self, config, sect):
        for k, v in configmap.items():
            nv = None
            if v[1] == float:
                nv = config.getfloat(sect, k, fallback=None)
            elif v[1] == str:
                nv = config.get(sect, k, fallback=None)
            if nv is not None:
                setattr(self, v[0], nv)

    def writeConfig(self, config, sect):
        for k, v in configmap.items():
            nv = getattr(self, v[0])
            if nv is None:
                continue
            if v[1] == float:
                nv = f2s(nv)
            elif v[1] == str:
                pass
            config.set(f"{sect}/k", nv)

