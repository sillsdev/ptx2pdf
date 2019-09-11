from ptxprint.runner import checkoutput
import struct, re


class TTFont:
    def __init__(self, fname, style):
        self.extrastyles = []
        while True:
            if style == "Medium":
                style = ""
            self.style = style
            pattern = fname + (":style="+style if style else ":style=Regular")
            pattern = pattern.replace("-", r"\-")
            files = checkoutput(["fc-list", pattern, "file"])
            f = re.split(r":\s", files, flags=re.M)[0].strip()
            if f != "" or style == "":
                break
            styles = style.split()
            self.extrastyles.append(styles[-1])
            style = " ".join(styles[:-1])
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
