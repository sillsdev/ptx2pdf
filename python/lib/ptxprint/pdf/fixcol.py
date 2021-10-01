
from ptxprint.pdfrw import *
from ptxprint.pdfrw.objects.pdfindirect import PdfIndirect
from ptxprint.pdfrw.objects.pdfname import BasePdfName
from ptxprint.pdfrw.uncompress import uncompress, streamobjects
from ptxprint.pdfrw.py23_diffs import zlib, convert_load, convert_store
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

    def parsepage(self, page, trailer, **kw):
        instrm = page.Contents
        if not isinstance(instrm, PdfArray):
            instrm = [instrm]
        for i in instrm:
            if isinstance(i, PdfIndirect):
                i = i.real_value()
            uncompress([i])
            strm = self.parsestream(trailer, i.stream, **kw)
            i.stream = strm

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
                    res.append(" ".join(fn(t, operands, **kw)))
                operands = []
        return "\r\n".join(res)


class PageCMYKState(PdfStreamParser):
    opmap = {'K': 'k', 'RG': 'rg'}
    def __init__(self, threshold, gstates):
        self.currgs = None
        self.threshold = threshold
        self.gstates = gstates
        self.testnumcols = False
        self.profile = None

    def setProfiles(self, inprofile, outprofile):
        self.profile = buildTransform(inprofile, outprofile, "RGB", "CMYK")

    def gs(self, op, operands, **kw):
        self.currgs = str(operands[-1])
        return operands + [op]

    def k(self, op, operands, **kw):
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

    def rg(self, op, operands, **kw):
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


class PageRGBState(PdfStreamParser):
    opmap = {'RG': 'rg', 'G': 'rg', 'g': 'rg'}

    def rg(self, op, operands, cskey=None, **kw):
        newop, newcs = (x.upper() if op[0] in "RG" else x for x in ("scn", "cs"))
        extras = []
        if cskey is not None:
            extras = ["/"+cskey, newcs]
        if op.lower() == "g":
            operands = operands * 3
        return extras + operands + [newop]


def compress(mylist):
    flate = PdfName.FlateDecode
    for obj in streamobjects(mylist):
        ftype = obj.Filter
        if ftype is not None:
            if not len(ftype):
                obj.Filter = None
            continue
        oldstr = obj.stream
        if obj.Binary is not None:
            obj.Binary = None
            newstr = convert_load(zlib.compress(oldstr))
        else:
            newstr = convert_load(zlib.compress(convert_store(oldstr)))
        if len(newstr) < len(oldstr) + 30:
            obj.stream = newstr
            obj.Filter = flate
            obj.DecodeParms = None

def fixpdfcmyk(trailer, threshold=1., **kw):
    for pagenum, page in enumerate(trailer.pages, 1):
        pstate = PageCMYKState(threshold, page.Resources.ExtGState)
        pstate.parsepage(page, trailer, **kw)
        annots = page.Annots
        if annots is not None:
            for a in annots:
                col = a.C
                if len(col) == 3:
                    newc = rgb2cmyk(*map(float, col))
                    a.C = PdfArray(list(map(PdfObject, newc)))

def fixpdfrgb(trailer, **kw):
    oi = trailer.Root.OutputIntents
    iccdat = None
    if oi is not None and len(oi):
        iccprofile = oi[0].DestOutputProfile
        if isinstance(iccprofile, PdfIndirect):
            iccprofile = iccprofile.real_value()
        uncompress([iccprofile], leave_raw=True)
        iccprofile[PdfName('Binary')] = True
        iccdat = iccprofile.stream
    if iccdat is None:
        iccfile = os.path.join(os.path.dirname(__file__), "..", "sRGB.icc")
        if os.path.exists(iccfile):
            with open(iccfile, "rb") as inf:
                iccdat = inf.read()
    if iccdat is None:
        return
    icc = PdfDict(indirect=True, Binary=True, N=3,
                  Alternate=PdfName("DeviceRGB"), stream=iccdat)
    for pagenum, page in enumerate(trailer.pages, 1):
        r = page.Resources
        if r is None:
            r = page.Resources = PdfDict()
        colrs = r.ColorSpace
        if colrs is None:
            colrs = r.ColorSpace = PdfDict()
        i = 0
        while "/CS"+str(i) in colrs:
            i += 1
        key = "CS"+str(i)
        iccclr = colrs[PdfName(key)] = PdfArray([PdfName("ICCBased"), icc])
        iccclr.indirect = True
        pstate = PageRGBState()
        pstate.parsepage(page, trailer, cskey=key, **kw)
        xobjs = r.XObject
        if xobjs is not None:
            for k, v in xobjs.items():
                if v.ColorSpace == "/DeviceRGB":
                    v.ColorSpace = iccclr

def fixhighlights(trailer, parlocs=None):
    annotlocs = {}
    res = []
    if parlocs is not None and os.path.exists(parlocs):
        with open(parlocs, encoding="utf-8") as inf:
            for l in inf.readlines():
                m = re.match(r"^\\(start|end)annot\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*)\}", l)
                if m:
                    pos = (float(m.group(3)) / 65536, float(m.group(4)) / 65536, int(m.group(5)))
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
                        newannots[ann.Ref] = [ann]
                        ann.QuadPoints = []
                    newannots[ann.Ref][-1].QuadPoints.append(list(map(float, ann.Rect)))
            else:
                newannots.setdefault(None, []).append(ann)
        pannots = PdfArray()
        pres = []
        for k, vannots in newannots.items():
            if k is None:
                page.Annots.extend(vannots)
            for v in vannots:
                q = []
                rect = []
                blefts = []
                brights = []
                margin = float(v.Margin) if v.Margin is not None else 0.
                # collect rectangles in QuadPoints
                if getattr(v, 'QuadPoints', None) is not None:
                    for i, r in enumerate(v.QuadPoints):
                        ymin = min(r[1], r[3])
                        ymax = max(r[1], r[3])
                        if k in annotlocs and i == 0 and annotlocs[k][0][2] == pagenum and ymin <= annotlocs[k][0][1] <= ymax:
                            xmin = annotlocs[k][0][0]
                        else:
                            xmin = min(r[0], r[2])
                        if k in annotlocs and i == len(v.QuadPoints) - 1 and annotlocs[k][1][2] == pagenum and ymin <= annotlocs[k][1][1] <= ymax:
                            xmax = annotlocs[k][1][0]
                        else:
                            xmax = max(r[0], r[2])
                        q += [xmin, ymin, xmax, ymin, xmin, ymax, xmax, ymax]
                        blefts += [(xmin - margin, ymax), (xmin - margin, ymin)]  # top to bottom
                        brights += [(xmax + margin, ymax), (xmax + margin, ymin)]
                        if i == 0:
                            rect = (xmin, ymin, xmax, ymax)
                        else:
                            rect = (min(rect[0], xmin), min(rect[1], ymin), max(rect[2], xmax), max(rect[3], ymax))
                if v.Subtype == "/Highlight":
                    v.QuadPoints = PdfArray(q)
                    v.Rect = PdfArray(rect)
                    v.Ref = None
                    pannots.append(v)
                elif v.Subtype == "/Background":
                    # convert rectangles to bounding polygon and graphics op stream
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

def fixpdffile(infile, outfile, colour="rgb", **kw):
    trailer = PdfReader(infile)

    fixhighlights(trailer, parlocs=kw.get('parlocs', None))
    if colour == "cmyk":
        fixpdfcmyk(trailer, threshold=kw.get('threshold', 1.), **kw)
    elif colour == "rgbx4":
        fixpdfrgb(trailer, **kw)

    meta = trailer.Root.Metadata
    if meta is not None:
        meta.Filter = []
    w = PdfWriter(outfile, trailer=trailer, version='1.4', compress=True, do_compress=compress)
    w.write()

