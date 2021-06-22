
from ptxprint.pdfrw import *
from ptxprint.pdfrw.objects.pdfindirect import PdfIndirect
from ptxprint.pdfrw.objects.pdfname import BasePdfName
from ptxprint.pdfrw.uncompress import uncompress
from PIL.ImageCms import applyTransform, buildTransform
from PIL import Image

import re, os

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

    def parsestream(self, rdr, strm, **kw):
        self.kw = kw
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

    def cm(self, op, operands):
        ins = self.kw.get('ins', None)
        print(ins)
        extras = [ins] if ins is not None and len(ins) else []
        self.kw['ins'] = None
        return operands + [op] + extras

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


def fixpdfcmyk(trailer, threshold=1., inserts=[], **kw):
    for pagenum, page in enumerate(trailer.pages, 1):
        ins = inserts[pagenum - 1] if pagenum <= len(inserts) else None
        pstate = PageState(threshold, page.Resources.ExtGState)
        instrm = page.Contents
        if not isinstance(instrm, PdfArray):
            instrm = [instrm]
        for i in instrm:
            if isinstance(i, PdfIndirect):
                i = i.real_value()
            uncompress([i])
            strm = pstate.parsestream(trailer, i.stream, ins=ins, **kw)
            i.stream = strm
        annots = page.Annots
        if annots is not None:
            for a in annots:
                col = a.C
                if len(col) == 3:
                    newc = rgb2cmyk(*map(float, col))
                    a.C = PdfArray(list(map(PdfObject, newc)))

def fixhighlights(trailer, parlocs=None):
    annotlocs = {}
    res = []
    if parlocs is not None and os.path.exists(parlocs):
        with open(parlocs) as inf:
            for l in inf.readlines():
                m = re.match(r"^\\(start|end)annot\{(.*?)\}\{(.*?)\}\{(.*?)\}", l)
                if m:
                    pos = (float(m.group(3)) / 65536, float(m.group(4)) / 65536)
                    if m.group(1) == "start":
                        annotlocs[m.group(2)] = (pos, pos)
                    else:
                        annotlocs[m.group(2)] = (annotlocs[m.group(2)][0], pos)
    for pagenum, page in enumerate(trailer.pages, 1):
        annots = page.Annots
        if annots is None:
            continue
        newannots = {}
        for ann in annots:
            if ann.Subtype in ("/Highlight", "/Background") and ann.QuadPoints is None:
                r = ann.Rect
                if ann.Ref is not None:
                    if ann.Ref not in newannots:
                        newannots[ann.Ref] = ann
                        ann.QuadPoints = []
                    newannots[ann.Ref].QuadPoints.append(list(map(float, ann.Rect)))
            else:
                newannots.setdefault(None, []).append(ann)
        pannots = PdfArray()
        pres = []
        for k, v in newannots.items():
            if k is None:
                page.Annots.extend(v)
            q = []
            rect = []
            blefts = []
            brights = []
            for i, r in enumerate(v.QuadPoints):
                ymin = min(r[1], r[3])
                ymax = max(r[1], r[3])
                if k in annotlocs and i == 0 and ymin <= annotlocs[k][0][1] <= ymax:
                    xmin = annotlocs[k][0][0]
                else:
                    xmin = min(r[0], r[2])
                if k in annotlocs and i == len(v.QuadPoints) - 1 and ymin <= annotlocs[k][1][1] <= ymax:
                    xmax = annotlocs[k][1][0]
                else:
                    xmax = max(r[0], r[2])
                q += [xmin, ymin, xmax, ymin, xmin, ymax, xmax, ymax]
                blefts += [(xmin, ymax), (xmin, ymin)]  # top to bottom
                brights += [(xmax, ymax), (xmax, ymin)]
                if i == 0:
                    rect = (xmin, ymin, xmax, ymax)
                else:
                    rect = (min(rect[0], xmin), min(rect[1], ymin), max(rect[2], xmax), max(rect[3], ymax))
            if v.Subtype == "/Highlight":
                print(newannots.get(k, ""), annotlocs.get(k, ""), q, rect)
                v.QuadPoints = PdfArray(q)
                v.Rect = PdfArray(rect)
                v.Ref = None
                pannots.append(v)
            elif v.Subtype == "/Background":
                brect = []
                for p in brights + list(reversed(blefts)):
                    if len(brect) > 1:
                        if brect[-2][0] == brect[-1][0] and brect[-1][0] == p[0]:
                            brect.pop()
                        elif p[0] != brect[-1][0]:
                            p = (p[0], brect[-1][1])
                    brect.append(p)
                col = v.C
                action = ["{} {} {} rg".format(*(simplefloat(float(c)) for c in col))]
                action.append("{} {} m".format(simplefloat(brect[0][0]), simplefloat(brect[0][1])))
                for p in brect[1:]:
                    action.append("{} {} l".format(simplefloat(p[0]), simplefloat(p[1])))
                action.append("h f")
                print(action)
                pres.append("\n".join(action))
            if len(pres):
                pres.insert(0, "q")
                pres.append("Q")
                page.Contents.insert(0, PdfDict(indirect=True, stream="\n".join(pres)))
        page.Annots = pannots if len(pannots) else None

def pagebbox(infile, pagenum=0):
    trailer = PdfReader(infile)
    if pagenum == 0:
        pagenum = 1
    pagenum -= 1
    pagenum = min(len(trailer.pages), pagenum)
    page = trailer.pages[pagenum]
    cropbox = page.inheritable.CropBox
    return cropbox

def fixpdffile(infile, outfile, **kw):
    trailer = PdfReader(infile)

    fixhighlights(trailer, parlocs=kw.get('parlocs', None))
    fixpdfcmyk(trailer, threshold=kw.get('threshold', 1.))

    meta = trailer.Root.Metadata
    if meta is not None:
        meta.Filter = []
    w = PdfWriter(outfile, trailer=trailer, version='1.4', compress=True)
    w.write()

