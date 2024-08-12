
from ptxprint.xdv.xdv import XDViReader
import re

class XDVFileReader(XDViReader):

    def __init__(self, fname, **kw):
        super().__init__(fname, **kw)
        self.allfonts = set()
        self.pics = set()

    def xfontdef(self, opcode, parm, data):
        (k, font) = super().xfontdef(opcode, parm, data)
        self.allfonts.add(font.name)
        return (k, font)

    def xxx(self, opcode, parm, data):
        txt = super().xxx(opcode, parm, data)
        fname = re.match(r"^pdf:image.*?\((.*?)\)$", txt[0])
        if fname:
            self.pics.add(fname.group(1))
        return (txt,)

def procxdv(inxdv):
    reader = XDVFileReader(inxdv)
    for a in reader.parse():
        pass
    return (reader.allfonts, reader.pics)
