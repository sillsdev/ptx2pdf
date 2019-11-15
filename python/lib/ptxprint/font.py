from ptxprint.runner import checkoutput
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

class TTFont:
    def __init__(self, name, style=""):
        p = Pango.font_description_from_string(name + (" " + style if style else ""))
        self.style = " ".join([self.style2str(p.get_weight()), self.style2str(p.get_style())]).strip()
        self.family = p.get_family()
        self.feats = {}
        self.names = {}
        self.getfname()
        self.readfont()

    def getfname(self):
        #pattern = '"' + self.family + '"' + 
        pattern = (":style=\""+self.style.title()+'"' if self.style else ":style=Regular")
        family = self.family.replace("-", r"\-")
        files = checkoutput(["fc-list", family, pattern, "file"], shell=1)
        self.filename = re.split(r":\s", files, flags=re.M)[0].strip()
        print(family, pattern, self.filename)
        return self.filename

    def readfont(self):
        self.dict = {}
        print(self.family, self.style, self.filename)
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
        print(version)
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
        print(self.featvals)
            

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
            # only get unicode strings
            if pid == 0 or (pid == 3 and (eid < 2 or eid == 10)):
                self.names[nid] = stringData[offset:offset+length].decode("utf_16_be")
            

    def style2str(self, style):
        return pango_styles.get(style, str(style))

    def __oldinit__(self, fname, style):
        self.extrastyles = []
        self.style = ""
        self.family = fname
        while True:
            if style == "Medium":
                style = ""
            if self.style == "":
                self.style = style
            pattern = '"' + self.fname() + '"' + (":style=\""+style.title()+'"' if style else ":style=Regular")
            pattern = pattern.replace("-", r"\-")
            files = checkoutput(["fc-list", pattern, "file"], shell=1)
            f = re.split(r":\s", files, flags=re.M)[0].strip()
            if f != "" or style == "":
                break
            # if no styles, try taking the last word of the filename as the style and so on
            if self.style == "":
                name = fname.split()
                fname = " ".join(name[:-1])
                self.style = name[-1]
                if fname == "":
                    break
                self.family = fname
            # if have styles, trim the style
            styles = style.split()
            self.extrastyles.append(styles[0])
            style = " ".join(styles[1:])
        self.dict = {}
        if f == "":
            return
        with open(f, "rb") as inf:
            dat = inf.read(12)
            (_, numtables) = struct.unpack(">4sH", dat[:6])
            dat = inf.read(numtables * 16)
            for i in range(numtables):
                (tag, csum, offset, length) = struct.unpack(">4sLLL", dat[i * 16: (i+1) * 16])
                self.dict[tag.decode("utf-8")] = [offset, length]

    def __contains__(self, k):
        return k in self.dict

    def fname(self):
        res = self.family
        if len(self.extrastyles):
            return res + " " + " ".join(self.extrastyles)
        else:
            return res
