#!/usr/bin/python3

from ptxprint.pdfrw import PdfReader, PdfWriter
from ptxprint.pdfrw.objects import PdfDict, PdfObject

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
        pr = d.Private
        if pr is None:
            continue
        category  = pr.Insertion
        if category is None:
            continue
        res.setdefault(category.lstrip("/"), []).append(p)
        trailer.pages.remove(p)
        noremove = False
        while (dad := p.Parent) is not None:
            try:
                if not noremove:
                    dad.Kids.remove(p)
                dad.Count = PdfObject(int(dad.Count) - 1)
            except ValueError:
                pass
            if len(dad.Kids) > 0:
                noremove = True
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
