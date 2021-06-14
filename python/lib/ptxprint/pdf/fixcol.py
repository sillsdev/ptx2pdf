
from ptxprint.pdfrw import *
from ptxprint.pdfrw.objects.pdfindirect import PdfIndirect
from ptxprint.pdfrw.objects.pdfname import BasePdfName
from ptxprint.pdfrw.uncompress import uncompress
from PIL.ImageCms import applyTransform, buildTransform
from PIL import Image

import re

def simplefloat(s, dp=3):
    return ("{:."+str(dp)+"f}").format(s).rstrip("0").rstrip(".")

def parsestrtok(s):
    if not isinstance(s, str):
        return s
    return PdfObject(s)

def rgb2cmyk(r, g, b):
    k = 1 - max(r, g, b)
    if k < 1.0:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
    else:
        c, m, y = (0, 0, 0)
    return [c, m, y, k]

class PdfStreamParser:

    def parsestream(self, rdr, strm):
        res = []
        operands = []
        toks = PdfTokens(strm)
        for t in toks:
            func = rdr.special.get(t)
            if func is not None:
                val = func(toks)
                if isinstance(val, PdfArray):
                    val = PdfArray([parsestrtok(x) for x in val])
                elif isinstance(val, PdfDict):
                    val = PdfDict({k: parsestrtok(v) for k, v in val.items()})
                operands.append(val)
        
            elif isinstance(t, (PdfString, BasePdfName)):
                operands.append(t)
            elif re.match(r"^[+-]?\d+(\.\d*)?", t):
                operands.append(t)
            elif t in ("true", "false", "null"):
                operands.append(t)
            else:       # must be an operator
                fn = getattr(self, self.opmap.get(t, t), None)
                if fn is None:
                    res.append(" ".join(str(x) for x in (operands + [t])))
                else:
                    res.append(" ".join(fn(t, operands)))
                operands = []
        return "\r\n".join(res)


class PageState(PdfStreamParser):
    opmap = {'K': 'k', 'RG': 'rg'}
    def __init__(self, threshold, gstates):
        self.currgs = None
        self.threshold = threshold
        self.gstates = gstates
        self.testnumcols = False
        self.profile = None

    def setProfiles(self, inprofile, outprofile):
        self.profile = buildTransform(inprofile, outprofile, "RGB", "CMYK")

    def gs(self, op, operands):
        self.currgs = str(operands[-1])
        return operands + [op]

    def k(self, op, operands):
        try:
            overprintme = self.overprinttest(operands)
        except (ValueError, TypeError):
            return operands + [op]
        extras = []
        if self.currgs is not None:
            overprint = dict.get(self.gstates[self.currgs], "/OP", "false") == "true"
            if overprint != (b >= self.threshold):
                newgs = (self.currgs[:-1] if self.currgs.endswith("a") else self.currgs+"a")[1:]
                extras = ["/"+newgs, "gs"]
                if newgs not in self.gstates:
                    opval = "true" if b >= self.threshold else "false"
                    opmval = 1 if b >= self.threshold else None
                    self._addgstate(newgs, self.currgs, op=opval, OP=opval, OPM=opmval)
                self.currgs = "/"+newgs
        return extras + operands + [op]

    def rg(self, op, operands):
        rgb = [float(x) for x in operands[-3:]]
        cmyk = self.rgb2cmyk(*rgb)
        newop = "k" if op.lower() == op else "K"
        return [simplefloat(x) for x in cmyk] + [newop]

    def _addgstate(self, newgs, gs, **kw):
        res = self.gstates[gs].copy()
        self.gstates[PdfName(newgs)] = res
        for k, v in kw.items():
            if v is not None:
                res[PdfName(k)] = PdfObject(v)

    def overprinttest(self, operands):
        vals = list(map(float, operands))
        if vals >= self.threshold:
            return True
        if self.testnumcols:
            numcols = sum(1 for v in vals if v > 0.)
            if numcols > 1:
                return True
        return False

    def rgb2cmyk(self, r, g, b):
        if self.profile is None:
            return rgb2cmyk(r, g, b)
        im = Image.new("RGB", (1, 1), (r*255, g*255, b*255))
        newim = applyTransform(im, self.profile)
        return newim.getpixel(0, 0)


def fixpdfcmyk(infile, outfile, threshold=1.):
    trailer = PdfReader(infile)

    for pagenum, page in enumerate(trailer.pages, 1):
        pstate = PageState(threshold, page.Resources.ExtGState)
        instrm = page.Contents
        if not isinstance(instrm, PdfArray):
            instrm = [instrm]
        for i in instrm:
            if isinstance(i, PdfIndirect):
                i = i.real_value()
            uncompress([i])
            strm = pstate.parsestream(trailer, i.stream)
            i.stream = strm

    PdfWriter(outfile, trailer=trailer).write()

