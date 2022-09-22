#!/usr/bin/python3

import math
from dataclasses import dataclass
from typing import Tuple, Union
from ptxprint.pdfrw.objects import PdfObject, PdfDict, PdfArray, PdfName, IndirectPdfDict
from ptxprint.pdfrw import PdfReader, PdfWriter, PageMerge
from ptxprint.pdfrw.uncompress import uncompress

k = 0.5522847498  # cp multiplier for 90 degree arc

def applycm(cm, p):
    return [cm[0] * p[0] + cm[2] * p[1] + cm[4],
            cm[1] * p[0] + cm[3] * p[1] + cm[5]]

def pdfqarc(p0, p3, pc, move=True):
    p1 = [p0[0] + (pc[0] - p0[0]) * k, p0[1] + (pc[1] - p0[1]) * k]
    p2 = [p3[0] - (p3[0] - pc[0]) * k, p3[1] - (p3[1] - pc[1]) * k]
    res = "{0[0]:.2f} {0[1]:.2f} m ".format(p0) if move else ""
    res += "{0[0]:.2f} {0[1]:.2f} {1[0]:.2f} {1[1]:.2f} {2[0]:.2f} {2[1]:.2f} c".format(p1, p2, p3)
    return res

cropstr = " ".join([pdfqarc([-0.7, 0], [0, 0.7], [-0.7, 0.7]),
                    pdfqarc([0, 0.7], [0.7, 0], [0.7, 0.7], False),
                    pdfqarc([0.7, 0], [0, -0.7], [0.7, -0.7], False),
                   "S", "-1 0 m", "1 0 l", "S", "0 1 m", "0 -1 l", "S"])

def mergedict(base, new):
    if base == new or new is None:
        return base
    if base.indirect:
        base = base.real_value()
    if new.indirect:
        new = new.real_value()
    for k, v in new.iteritems():
        if k not in base:
            base[k] = v
            continue
        if v == base[k]:
            continue
        if isinstance(v, PdfDict):
            mergedict(base[k], v)
        elif isinstnace(v, PdfArray):
            base[k].extend([x for x in v if x not in base[k]])
        else:
            raise ValueError(f"Dictionary collision at {k} of {base[k]} and {v}")
    return base

def mapnamepages(names, pagemap):
    if names is None:
        return
    if names.Kids is not None:
        for k in names.Kids:
            mapnamepages(k, pagemap)
    if names.Names is not None:
        for v in names.Names[1::2]:
            if v[0].pid in pagemap:
                pm = pagemap[v[0].pid]
                v[0] = pm[0]
                if v[1] == '/XYZ':
                    (x, y) = applycm(pm[1], (float(v[2]), float(v[3])))
                    v[2] = PdfObject("{:.2f}".format(x))
                    v[3] = PdfObject("{:.2f}".format(y))

def buildPagesTree(pages, n=8):
    if len(pages) < n:
        res = IndirectPdfDict(Type=PdfName.Pages,
                                  Count=PdfObject(len(pages)),
                                  Kids = pages)
        for p in pages:
            p.Parent = res
        return res
    else:
        collect = []
        x = (len(pages) + n - 1) // n
        res = IndirectPdfDict(Type=PdfName.Pages, Count=len(pages), Kids=collect)
        for i in range(n):
            p = buildPagesTree(pages[i*x:(i+1)*x], n=n)
            collect.append(p)
            p.Parent = res
        return res


@dataclass
class PL:
    x: int
    y: int
    page: int = 0
    invert: int = 0

@dataclass
class Size:
    w: float
    h: float

    def swap(self):
        self.w, self.h = self.h, self.w

layouts = {
    4:  (PL(0, 1), PL(0, 0, 1), PL(0, 1, 1), PL(0, 0)),                     # 4 1           # 2 3

    8:  (PL(1, 0), PL(0, 0, 1), PL(0, 1, 1, 1), PL(1, 1, 0, 1),             # 5 4           # 3 6
         PL(0, 1, 0, 1), PL(1, 1, 1, 1), PL(1, 0, 1), PL(0, 0)),            # 8 1           # 2 7

    16: (PL(1, 3), PL(1, 0, 1), PL(1, 3, 1), PL(1, 0),                      # 5 12  9 8     # 7 10 11 6
         PL(0, 0, 0, 1), PL(0, 3, 1, 1), PL(0, 0, 1, 1), PL(0, 3, 0, 1),    # 4 13 16 1     # 2 15 14 3
         PL(0, 2, 0, 1), PL(0, 1, 1, 1), PL(0, 2, 1, 1), PL(0, 1, 0, 1),
         PL(1, 1), PL(1, 2, 1), PL(1, 1, 1), PL(1, 2))

}

class Signature:
    def __init__(self, srcsize, tgtsize, pages, sigsheets, fold, hascrops=False):
        self.hascrops = hascrops
        self.src = Size(*srcsize)
        self.tgt = Size(*tgtsize)
        self.mbox = PdfArray([0, 0, self.tgt.w, self.tgt.h])
        self.pages = pages * 2
        self.sigsheets = sigsheets
        self.rotate = (int(math.log2(self.pages)) & 1) == 0
        self.fold = fold if self.pages != 4 else 0
        if self.rotate:
            self.numy = int(math.sqrt(self.pages))
            self.numx = self.numy // 2
            self.cell = Size(self.tgt.h / self.numy, self.tgt.w / self.numx)
            self.margin = Size(self.cell.w - self.src.w,
                               0.5 * (self.cell.h - self.src.h))        # outer cut margin
        else:
            self.numx = self.numy = int(math.sqrt(self.pages / 2))
            mult = 1. / self.numx
            self.cell = Size(mult * self.tgt.w, mult * self.tgt.h)
            self.margin = Size((self.cell.w - self.src.w),
                               0.5 * (self.cell.h - self.src.h))
        if (self.pages > 8 and self.margin.w < self.fold) or (self.pages > 4 and self.margin.h < self.fold):
            raise OverflowError("Margin ({0.w:.2f} pt x {0.h:.2f} pt) less than folding margin {1:.2f} pt".format(self.margin, self.fold))

    def cm(self, i):
        self.crops = []
        res = [0, 1, -1, 0, 0, 0] if self.rotate else [1, 0, 0, 1, 0, 0]
        pos = layouts[self.pages][i]
        if pos.invert != 0:
            res = [-x for x in res]
            xcell, ycell = (pos.x, pos.y + 1) if self.rotate else (pos.x + 1, pos.y + 1)
        else:
            xcell, ycell = (pos.x + 1, pos.y) if self.rotate else (pos.x, pos.y)
        if self.rotate:
            res[4] = xcell * self.cell.h
            res[5] = ycell * self.cell.w
        else:
            res[4] = xcell * self.cell.w
            res[5] = ycell * self.cell.h

        bindleft = i & 1 == 0
        if bindleft:
            trans = [0., self.margin.h]
        else:
            trans = [self.margin.w, self.margin.h]
        res = res[:4] + [res[0] * trans[0] + res[2] * trans[1] + res[4],
                         res[1] * trans[0] + res[3] * trans[1] + res[5]]
        if bindleft:
            self.docropmark(res, [self.src.w, 0], 4)
            self.docropmark(res, [self.src.w, self.src.h], 3)
        else:
            self.docropmark(res, [0, 0], 1)
            self.docropmark(res, [0, self.src.h], 2)
        return res

    def pagenum(self, i, maxpages, rtl):
        ''' returns (signum, output_pnum, output_pnum_within_sig) '''
        if rtl:
            tmaxpages = ((maxpages + self.pages - 1) // self.pages) * self.pages
            i = tmaxpages - i
        if self.sigsheets == 0:
            ppsig = ((maxpages + self.pages - 1) // self.pages) * self.pages
        else:
            ppsig = self.pages * self.sigsheets
        sigid = i // ppsig          # signature number
        n = i - sigid * ppsig       # page number within signature
        normnum = n if n < ppsig // 2 else ppsig - n - 1
        sheetnum = normnum // (self.pages // 2)     # sheet number within signature
        sigindex = n - sheetnum * (self.pages // 2) if n < ppsig // 2 else self.pages - (ppsig - n - sheetnum * (self.pages // 2))
        opnum = sigid * self.sigsheets * 2 + sheetnum * 2 + layouts[self.pages][sigindex].page
        # print(f"pagenum({i}, {maxpages}) = ({sigid}, {opnum}, {sigindex}) [{sheetnum=}, {n=}, {normnum=}]")
        return (sigid, opnum, sigindex)

    def docropmark(self, cm, p, n):
        scale = min(self.margin.w, self.margin.h)   # 3mm outside margin for printing
        if scale < 0:
            return
        if scale > 18:
            scale = 18
        x, y = applycm(cm, p)
        w = 0.1 / scale         # make them .1pt thick
        s = scale if (n & 2) != 0 else -scale
        xs = s if (n & 1) != 0 else 0.
        ys = 0. if (n & 1) != 0 else s
        ccm = [xs, ys, -ys, xs, p[0], p[1]]
        cstr = " q {:.2f} w ".format(w) + ("{:.2f} " * 6).format(*ccm) + " cm " + cropstr + " Q"
        self.crops.append(cstr)

    def appendpage(self, i, page, p1, p2, maxpages):
        sigid, sigsheet, signum = self.pagenum(i, maxpages)
        # print(f"{i=} {sigid=} {sigsheet=} {signum=}")
        cm = self.cm(signum)
        pnum = layouts[self.pages][signum].page
        p = p2 if pnum == 1 else p1
        if self.hascrops:
            uncompress(page.Contents)
            s = page.Contents[0].stream
            page.Contents[0].stream = s + "\n".join(self.crops)
            scale = min(self.margin.w, self.margin.h)
            if scale > 0:
                if scale > 18:
                    scale = 18
            bb = page.MediaBox
            page.MediaBox = PdfArray([float(bb[0]) - scale, float(bb[1]) - scale, float(bb[2]) + scale, float(bb[3]) + scale])
        p.add(page)
        p.subpages.append(getattr(page, 'pid', 0))
        pobj = p[-1]
        pobj.Matrix = cm

def make_signatures(trailer, outwidth, outheight, num, sigsheets, foldmargin, hascrops, rtl, outfname=None):
    if isinstance(trailer, str):
        trailer = PdfReader(trailer)
    writer = PdfWriter(outfname)
    pages = trailer.pages
    mbox = [float(x) for x in pages[0].MediaBox]
    width = mbox[2] - mbox[0]
    height = mbox[3] - mbox[1]
    sig = Signature([width, height], [outwidth, outheight], num, sigsheets, foldmargin, hascrops)
    merges = []
    for i, p in enumerate(pages):
        p.pid = i
        sign, sigi, sigp = sig.pagenum(i, len(pages), rtl)
        if sigi & 1 == 0:
            sigi += 1
        while sigi >= len(merges):
            m = PageMerge()
            merges.append(m)
            m.subpages = []
            m.crops = []
        p1, p2 = merges[sigi-1:sigi+1]
        sig.appendpage(i, p, p1, p2, len(pages))
    pagemap = {}
    for m in merges:
        m.mbox = sig.mbox
        p = m.render()
        p.Rotate = sig.rotate * 90
        writer.addpage(p)
        #import pdb; pdb.set_trace()
        for i, oldp in enumerate(m.subpages):
            pagemap[oldp] = (p, m[i].Matrix)
    if trailer.Root.Names is not None:
        mapnamepages(trailer.Root.Names.Dests, pagemap)
    trailer.Root.Pages=buildPagesTree(writer.pagearray)
    writer.trailer = trailer
    if outfname is not None:
        writer.write()
    return writer


if __name__ == "__main__":
    import argparse

    pagesizes = {
        'a4': (595, 842),
        'a4b': (635, 882),
        'ltr': (612, 792),
        'lgl': (612, 1008),
        'a3': (842, 1191),
        'a3b': (862, 1211),
        'a2': (1191, 1684),
        'a2b': (1211, 1704)
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('infile',nargs='?',help='Input PDF file')
    parser.add_argument('-o','--outfile',help='Output PDF file (required if input PDF file)')
    parser.add_argument('-n','--num',type=int,help="Number of pages per side")
    parser.add_argument('-s','--size',help='Paper size: name or widthxheight')
    parser.add_argument('--outheight',type=float,help="Target page height (in pts)")
    parser.add_argument('--outwidth',type=float,help="Target page width (in pts)")
    parser.add_argument('-S','--sigsheets',type=int,default=1,help='Number of sheets per signature')
    parser.add_argument('-f','--fold',type=float,default=0.,help='Minimum fold cut margin')
    parser.add_argument('-c','--crops',action="store_true",help="Add cropmarks")
    parser.add_argument('-H','--height',type=float,help="Source page height")
    parser.add_argument('-W','--width',type=float,help="Source page width")
    args = parser.parse_args()

    if args.size is not None:
        if 'x' in args.size:
            args.outwidth, args.outheight = (float(x.strip()) for x in args.size.split('x'))
        elif args.size.lower() in pagesizes:
            args.outwidth, args.outheight = pagesizes[args.size.lower()]
        elif args.size.lower().endswith('l') and args.size.lower()[:-1] in pagesizes:
            args.outheight, args.outwidth = pagesizes[args.size.lower()[:-1]]
        else:
            print(f"Unknown paper size: {args.size}. Keeping going and will probably crash")
    if not args.infile:
        sig = Signature([args.width, args.height], [args.outwidth, args.outheight],
                    args.num, args.sigsheets, args.fold)
        print(f"{sig.margin=}, {sig.cell=}, num=({sig.numx}, {sig.numy})")
        for i in range(2*args.num):
            print(i, sig.pagenum(i, args.num), sig.cm(i), sig.crops)
    elif not args.outfile:
        print("Must specify an output file if processing an input file")
    else:
        make_signatures(args.infile, args.outwidth, args.outheight, args.num,
                        args.sigsheets, args.fold, args.crops, outfname=args.outfile)
