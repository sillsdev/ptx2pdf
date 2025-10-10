from ptxprint.utils import coltoonemax, _
from ptxprint.pdf.fixcol import fixpdffile, compress, outpdf
from ptxprint.pdfrw import PdfReader, PdfWriter
from ptxprint.pdfrw.objects import PdfDict, PdfString, PdfArray, PdfName, IndirectPdfDict, PdfObject
from ptxprint.pdf.pdfsanitise import split_pages
from ptxprint.pdf.pdfsig import make_signatures, buildPagesTree
from io import BytesIO as cStringIO
import os, re
import logging

logger = logging.getLogger(__name__)


_pdfmodes = {
    'rgb': ("Screen", "Digital"),
    'cmyk': ("CMYK", "Transparency")
}

_unitpts = {
    'mm': 2.845275591,
    'in': 72.27,
    'pt': 1
}

def procpdf(outfname, pdffile, ispdfxa, doError, createSettingsZip, **kw):
    res = {}
    opath = outfname.replace(".tex", ".prepress.pdf")
    ext = None
    outpdfobj = None
    coverfile = None
    if kw.get('burst', False) or kw.get('cover', False):
        inpdf = PdfReader(opath)
        extras = split_pages(inpdf)
        logger.debug("Bursting: " + " ".join(extras.keys()))
        for k, eps in extras.items():
            bpdfname = pdffile.replace(".pdf", f"_{k}.pdf")
            if k == 'cover':
                if kw.get('cover', False):
                    coverfile = bpdfname
                else:
                    continue
            elif not kw.get('burst', False):
                continue
            logger.debug(f"Pulling out {k} into {bpdfname} from {opath}")
            bpdf = PdfReader(source=inpdf.source, trailer=inpdf)
            bpdf.Root = bpdf.Root.copy()
            bpdf.Root.Pages = buildPagesTree(eps)
            # bpdf.Root.Pages = IndirectPdfDict(Type=PdfName("Pages"), Count=PdfObject(len(eps)), Kids=PdfArray(eps))
            bpdf.Root.Names = None
            bpdf.Root.Outlines = None
            bpdf.private.pages = eps
            for v in eps:
                v.parent = bpdf.Root.Pages
            if ispdfxa == "Screen":
                outpdf(bpdf, bpdfname)
            else:
                fixpdffile(bpdf, bpdfname, colour="cmyk", copy=True)
            res[k] = bpdfname
        outpdfobj = PdfWriter(None, trailer=inpdf)
    colour = None
    params = {}
    if ispdfxa == "Spot":
        colour = "spot"
        params = {'color': coltoonemax(kw.get('spotcolor', 'rgb(0, 0, 0)')),
                  'range': float(kw.get('spottolerance', 1)) / 100.}
    elif ispdfxa == "Screen":
        pass
    elif ispdfxa in _pdfmodes['rgb']:
        colour = "rgbx4"
    elif ispdfxa in _pdfmodes['cmyk']:
        colour = "cmyk"
    else:
        colour = ispdfxa.lower()
    if colour is not None:
        logger.debug(f"Fixing colour for {colour}")
        if ext is None:
            ext = "_"+colour
        try:
            outpdfobj = fixpdffile((outpdfobj._trailer if outpdfobj else opath), None,
                        colour=colour,
                        parlocs = outfname.replace(".tex", ".parlocs"), **params)
        except ValueError:
            return {}
    nums = int(kw.get('pgsperspread', 1))
    if nums > 1:
        if ext is None:
            ext = "_{}up".format(nums)
        psize = kw.get('sheetsize', "21omm, 297mm (A4)").split(",")
        paper = []
        for p in psize:
            m = re.match(r"^\s*([\d.]+)\s*(mm|in|pt)", p)
            if m:
                paper.append(float(m.group(1)) * float(_unitpts[m.group(2)])) 
            else:
                paper.append(0.)
        sigsheets = int(kw.get('sheetsinsigntr', 0))
        foldmargin = int(kw.get('foldcutmargin', 0)) * _unitpts['mm']
        logger.debug(f"Impositioning onto {nums} pages. {sigsheets=}, {foldmargin=} from {paper[0]} to {paper[1]}")
        try:
            outpdfobj = make_signatures((outpdfobj._trailer if outpdfobj else opath),
                                 paper[0], paper[1], nums,
                                 sigsheets, foldmargin, kw.get('cropmarks', False), kw.get('ifrtl', 'false').lower() == 'true',
                                 kw.get('foldfirst', False))
        except OverflowError as e:
            print(e)
            doError(_("Try adjusting the output paper size to account for the number of pages you want"),
                                 title=_("Paper Size Error"), secondary=str(e), threaded=True)
            return {}
    if kw.get('inclsettings', False):
        if ext is None:
            ext = ""
        logger.debug("Adding settings to the pdf")
        zio = cStringIO()
        createSettingsZip(zio)
        if len(zio.getvalue()):
            if outpdfobj is None:
                outpdfobj = PdfWriter(None, trailer=PdfReader(opath))
            if outpdfobj.trailer.Root.PieceInfo is None:
                p = PdfDict()
                outpdfobj.trailer.Root.PieceInfo = p
            else:
                p = output.trailer.Root.PieceInfo
            pdict = PdfDict(LastModified= "D:" + kw.get("pdfdate_", ""))
            pdict.Private = PdfDict()
            pdict.Private.stream = zio.getvalue()
            pdict.Private.Binary = True
            p.ptxprint = pdict
        zio.close()

    if opath != pdffile:
        if os.path.exists(pdffile):
            os.remove(pdffile)
        try:
            os.rename(opath, pdffile)
        except (FileNotFoundError, PermissionError):
            pass
    if outpdfobj is not None:
        pdffile = pdffile.replace(".pdf", ext+".pdf")
        if ext != "":
            res[' Finished'] = pdffile
        outpdfobj.fname = pdffile
        outpdfobj.compress = True
        outpdfobj.do_compress = compress
        outpdfobj.write()
    return res

