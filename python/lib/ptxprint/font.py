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

class TTFont:
    def __init__(self, name, style=""):
        p = Pango.font_description_from_string(name + (" " + style if style else ""))
        self.style = " ".join([self.style2str(p.get_weight()), self.style2str(p.get_style())]).strip()
        self.family = p.get_family()
        self.getfname()
        self.readfont()

    def getfname(self):
        pattern = '"' + self.family + '"' + (":style=\""+self.style.title()+'"' if self.style else ":style=Regular")
        pattern = pattern.replace("-", r"\-")
        files = checkoutput(["fc-list", pattern, "file"], shell=1)
        self.filename = re.split(r":\s", files, flags=re.M)[0].strip()
        print(pattern, self.filename)
        return self.filename

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
