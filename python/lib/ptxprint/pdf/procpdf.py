from ptxprint.utils import coltoonemax, _
from ptxprint.pdf.fixcol import fixpdffile, compress, outpdf
from ptxprint.pdfrw import PdfReader, PdfWriter
from ptxprint.pdfrw.objects import PdfDict, PdfString, PdfArray, PdfName, IndirectPdfDict, PdfObject
from ptxprint.pdf.pdfsanitise import split_pages
from ptxprint.pdf.pdfsig import make_signatures, buildPagesTree
from io import BytesIO as cStringIO
import os, re, time
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

def make_stream(content):
    s = IndirectPdfDict()
    s.stream = content
    return s

def safeRename(infile, outfile):
    try:
        if os.path.exists(outfile):
            os.remove(outfile)
        os.rename(infile, outfile)
    except (FileNotFoundError, PermissionError):
        pass

def procpdf(outfname, pdffile, ispdfxa, doError, createSettingsZip, **kw):
    res = {}
    opath = pdffile
    ext = None
    outpdfobj = None
    origobj = None
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

    paper = []
    psize = (kw.get('sheetsize', None) or "210mm, 297mm (A4)").split(",")
    for p in psize:
        m = re.match(r"^\s*([\d.]+)\s*(mm|in|pt)", p)
        if m:
            paper.append(float(m.group(1)) * float(_unitpts[m.group(2)])) 
        else:
            paper.append(0.)

    nums = int(kw.get('pgsperspread', 1))
    if nums > 1:
        if ext is None:
            ext = "_{}up".format(nums)
        else:
            ext = "{}_{}up".format(ext, nums)
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
    else:  # nums is 1
        scale_to_fit = bool(kw.get("scaletofit", False))
        if scale_to_fit:
            src = outpdfobj._trailer if outpdfobj else PdfReader(opath)
            if outpdfobj is None:
                outpdfobj = PdfWriter(None, trailer=src)
            target_w, target_h = paper[0], paper[1]
            for page in src.pages:
                mb = page.MediaBox
                if mb is None:
                    continue
                pg_w = float(mb[2]) - float(mb[0])
                pg_h = float(mb[3]) - float(mb[1])
                if pg_w == 0 or pg_h == 0:
                    continue
                scale = min(target_w / pg_w, target_h / pg_h)
                if abs(scale - 1.0) < 1e-4:
                    continue
                tx = (target_w - pg_w * scale) / 2
                ty = (target_h - pg_h * scale) / 2
                matrix_op = "{} {} {} {} {} {} cm\n".format(*[round(v, 6) for v in [scale, 0, 0, scale, tx, ty]])
                save  = make_stream("q\n" + matrix_op)
                restore = make_stream("\nQ\n")
                existing = page.Contents
                if existing is None:
                    page.Contents = PdfArray([save, restore])
                elif isinstance(existing, PdfArray):
                    page.Contents = PdfArray([save] + list(existing) + [restore])
                else:
                    page.Contents = PdfArray([save, existing, restore])
                page.MediaBox = PdfArray([PdfObject(0), PdfObject(0),
                                        PdfObject(round(target_w, 4)),
                                        PdfObject(round(target_h, 4))])
                page.CropBox = None

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
                p = outpdfobj.trailer.Root.PieceInfo
            pdict = PdfDict(LastModified= "D:" + kw.get("pdfdate_", ""))
            pdict.Private = PdfDict()
            pdict.Private.stream = zio.getvalue()
            pdict.Private.Binary = True
            p.ptxprint = pdict

            if nums > 1 and os.path.exists(opath):
                origobj = PdfWriter(None, trailer=PdfReader(opath))
                if origobj.trailer.Root.PieceInfo is None:
                    op = PdfDict()
                    origobj.trailer.Root.PieceInfo = op
                else:
                    op = origobj.trailer.Root.PieceInfo
                # Fresh dict — do NOT share pdict across writers
                origpdict = PdfDict(LastModified= "D:" + kw.get("pdfdate_", ""))
                origpdict.Private = PdfDict()
                origpdict.Private.stream = zio.getvalue()
                origpdict.Private.Binary = True
                op.ptxprint = origpdict
                origobj.fname = opath
                origobj.compress = True
                origobj.do_compress = compress
                # Note: deliberately NOT calling origobj.write() here
        zio.close()

    if outpdfobj is not None:
        if opath != pdffile:
            if os.path.exists(opath):
                safeRename(opath, pdffile)
        if ext is not None and ext != "":
            pdffile = pdffile.replace(".pdf", ext+".pdf")
            res[' Finished'] = pdffile
        elif opath == pdffile:
            opath = os.path.normpath(pdffile).replace(".pdf", ".prepress.pdf")
            safeRename(pdffile, opath)
            res[' Original'] = opath
        if kw.get("output_filepath"):
            pdffile = kw.get("output_filepath")
        outpdfobj.fname = pdffile
        outpdfobj.compress = True
        outpdfobj.do_compress = compress
        outpdfobj.write()

    # Write the settings-augmented 1-up *after* the 2-up has been serialised, so 
    # its lazy references into opath still resolve to the original xetex output.
    if origobj is not None:
        origobj.write()

    return res

