from ptxprint.runner import call
import struct


class TTFont:
    def __init__(self, fname, style):
        while True:
            if style == "Medium":
                style = ""
            pattern = fname + (":style="+style if style else ":style=Regular")
            pattern = pattern.replace("-", r"\-")
            files = call(["fc-list", pattern, "file"])
            f = files.split("\n")[0].strip()[:-1]
            if f != "" or style == "":
                break
            style = " ".join(style.split()[:-1])
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
