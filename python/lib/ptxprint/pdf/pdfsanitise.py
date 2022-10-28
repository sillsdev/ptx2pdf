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

def sanitise(trailer, opath=None, forced=True):
    if isinstance(trailer, str):
        trailer = PdfReader(trailer)
    changed = ensure_contents(trailer)
    if (changed or force) and opath is not None:
        outpdf = PdfWriter(None, trailer=trailer)
        outpdf.fname = opath
        outpdf.write()
    return changed
