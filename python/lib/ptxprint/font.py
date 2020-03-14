from ptxprint.runner import fclist, checkoutput
import struct, re
from gi.repository import Pango

pango_styles = {Pango.Style.ITALIC: "italic",
    Pango.Style.NORMAL: "",
    Pango.Weight.ULTRALIGHT: "ultra light",
    Pango.Weight.LIGHT: "light",
    Pango.Weight.NORMAL: "",
    Pango.Weight.BOLD: "bold",
    Pango.Weight.ULTRABOLD: "ultra bold",
    Pango.Weight.HEAVY: "heavy"
}

def num2tag(n):
    if n < 0x200000:
        return str(n)
    else:
        return struct.unpack('4s', struct.pack('>L', n))[0].replace(b'\000', b'').decode()

class TTFontCache:
    def __init__(self):
        self.cache = {}
        files = checkoutput(["fc-list", ":file"])
        for f in files.split("\n"):
            if ": " not in f:
                continue
            try:
                (path, full) = f.strip().split(": ")
                if ":style=" in full:
                    (name, style) = full.split(':style=')
                    # print(f.encode("unicode_escape"))
                else:
                    name = full
                    style = ""
                if "," in name:
                    # print(f.encode("unicode_escape"))
                    names = name.split(",")
                    # print names.encode("unicode_escape")
                else:
                    names = [name]
                if "," in style:
                    styles = style.split(",")
                    # print styles.encode("unicode_escape")
                else:
                    styles = [style]
            except ValueError:
                raise SyntaxError("Can't parse: {}".format(f).encode("unicode_escape"))
            for n in names:
                for s in styles:
                    # if n == "Awami Nastaliq":
                        # print(n.encode("unicode_escape"),s.encode("unicode_escape"))
                    self.cache["{}|{}".format(n, s)] = path
        # print("FontCache size:" + str(len(self.cache)))

    def find(self, name, style):
        orgname = name
        orgstyle = style.title()
        if style == "":
            style = "Regular"
        else:
            style = style.title()
        res = self.get(name, style)
        while res is None:
            cn = name.split(" ")
            name = " ".join(cn[:-1])
            if style == "Regular":
                style = ""
            style = cn[-1].title() + (" " + style if len(style) else "")
            if not len(name):
                return (None, orgname, orgstyle)
            res = self.get(name, style)
            if res is None:
                res = self.get(name, "Regular")
                if res is not None:
                    break
        return (res, name, style)

    def get(self, name, style):
        if len(style) == 0:
            style = "Regular"
        k = "{}|{}".format(name, style)
        # print(k,self.cache.get(k, None))
        return self.cache.get(k, None)

fontcache = TTFontCache()

class TTFont:
    def __init__(self, name, style=""):
        p = Pango.font_description_from_string(name + (" " + style if style else ""))
        self.style = " ".join([self.style2str(p.get_weight()), self.style2str(p.get_style())]).strip()
        self.family = p.get_family()
        self.filename = fontcache.get(self.family.replace("-", "\\-"), self.style.title())
        self.feats = {}
        self.featvals = {}
        self.names = {}
        if self.filename is not None:
            self.readfont()
        else:
            self.dict = {}

    def readfont(self):
        self.dict = {}
        if self.filename == "":
            return
        with open(self.filename, "rb") as inf:
            dat = inf.read(12)
            (_, numtables) = struct.unpack(">4sH", dat[:6])
            dat = inf.read(numtables * 16)
            for i in range(numtables):
                (tag, csum, offset, length) = struct.unpack(">4sLLL", dat[i * 16: (i+1) * 16])
                self.dict[tag.decode("utf-8")] = [offset, length]
            self.readNames(inf)
            self.readFeat(inf)

    def readFeat(self, inf):
        self.feats = {}
        self.featvals = {}
        if 'Feat' not in self.dict:
            return
        inf.seek(self.dict['Feat'][0])
        data = inf.read(self.dict['Feat'][1])
        (version, subversion) = struct.unpack(">HH", data[:4])
        numFeats, = struct.unpack(">H", data[4:6])
        for i in range(numFeats):
            if version >= 2:
                (fid, nums, _, offset, flags, lid) = struct.unpack(">LHHLHH", data[12+16*i:28+16*i])
            else:
                (fid, nums, offset, flags, lid) = struct.unpack(">HHLHH", data[12+12*i:24+12*i])
            self.feats[num2tag(fid)] = self.names.get(lid, "")
            valdict = {}
            self.featvals[num2tag(fid)] = valdict
            for j in range(1, nums):
                val, lid = struct.unpack(">HH", data[offset + 4*j:offset + 4*(j+1)])
                valdict[val] = self.names.get(lid, "")
            
    def readNames(self, inf):
        self.names = {}
        if 'name' not in self.dict:
            return
        inf.seek(self.dict['name'][0])
        data = inf.read(self.dict['name'][1])
        fmt, n, stringOffset = struct.unpack(b">HHH", data[:6])
        stringData = data[stringOffset:]
        data = data[6:]
        for i in range(n):
            if len(data) < 12:
                break
            (pid, eid, lid, nid, length, offset) = struct.unpack(b">HHHHHH", data[12*i:12*(i+1)])
            # only get unicode strings (US English)
            if (pid == 0 and lid == 0) or (pid == 3 and (eid < 2 or eid == 10) and lid == 1033):
                self.names[nid] = stringData[offset:offset+length].decode("utf_16_be")

    def style2str(self, style):
        return pango_styles.get(style, str(style))

    def __contains__(self, k):
        return k in self.dict

    def fname(self):
        res = self.family
        if len(self.extrastyles):
            return res + " " + " ".join(self.extrastyles)
        else:
            return res
