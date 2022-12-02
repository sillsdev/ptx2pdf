#!/usr/bin/python3

from ptxprint.pdfrw import PdfReader, PdfWriter
from ptxprint.pdfrw.objects import PdfDict

def ensure_contents(trailer):
    changed = False
    for p in trailer.pages:
        try:
            c = p.Contents
        except KeyError:
            c = None
        if c is None:
            changed = True
            c = PdfDict(indirect=True)
            c._stream = ""
            c.Length = 0
            p.Contents = c
    return changed

def split_pages(trailer):
    res = {}
    for p in list(trailer.pages):
        if p.PieceInfo is None:
            continue
        d = p.PieceInfo.ptxprint
        if d is None:
            continue
        category  = d.Insert
        if fname is None:
            continue
        res.setdefault(category, []).append(p)
        trailer.pages.remove(p)
        while dad := p.parent is not None:
            try:
                dad.Kids.remove(p)
            except ValueError:
                pass
            if len(dad.Kids) > 0:
                break
            p = dad
    return res

def sanitise(trailer, opath=None, forced=True):
    if isinstance(trailer, str):
        trailer = PdfReader(trailer)
    changed = ensure_contents(trailer)
    if (changed or forced) and opath is not None:
        outpdf = PdfWriter(None, trailer=trailer)
        outpdf.fname = opath
        outpdf.write()
    return changed
