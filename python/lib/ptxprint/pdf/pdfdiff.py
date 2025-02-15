
import os, argparse
from PIL import Image, ImageChops, ImageEnhance, ImageOps
from ptxprint.utils import _
import logging
logger = logging.getLogger(__name__)

def createDiff(pdfname, othername, outname, doError, color=None, onlydiffs=True, 
                maxdiff=False, oldcolor=None, limit=0, dpi=0, **kw):
    if color is None or not len(color):
        color = (240, 0, 0)
    if oldcolor is None or not len(oldcolor):
        oldcolor = (0, 0, 240)
    if not os.path.exists(othername):
        return 2
    try:
        ingen = pdfimages(pdfname, dpi=dpi)
        ogen = pdfimages(othername, dpi=dpi)
    except ImportError:
        return 1
    results = []
    hasdiffs = False
    for iimg in ingen:
        oimg = next(ogen, None)
        if oimg is None:
            break
        dmask = ImageChops.difference(oimg, iimg).convert("L")
        dval = sum([i * x / 256. for i, x in enumerate(dmask.histogram()) if i > 12])
        logger.debug(f"Difference val = {dval} size({dmask.getbbox()})")
        if not dmask.getbbox() or dval < 2.:
            if onlydiffs:
                continue
        elif dmask.size != iimg.size:
            doError(_("Page sizes differ between output and base. Cannot create a difference."),
                threaded=True, title=_("Difference Error"))
            return 3
        else:
            hasdiffs = True
        if maxdiff:
            dmask = dmask.point(lambda x: 255 if x else 0)
        diffimg = ImageChops.subtract(oimg, iimg, scale=0.5, offset=127).convert("L")    # old - new
        overlay = ImageOps.colorize(diffimg, color, oldcolor, mid=(255, 255, 255))
        #translucent = Image.new("RGB", iimg.size, color)
        enhancec = ImageEnhance.Contrast(iimg)
        enhanceb = ImageEnhance.Brightness(enhancec.enhance(0.7))
        nimg = enhanceb.enhance(1.5)
        nimg.paste(overlay, (0, 0), dmask)
        results.append(nimg)
        if limit > 0 and len(results) >= limit:
            break
    if hasdiffs and len(results):
        results[0].save(outname, format="PDF", save_all=True, append_images=results[1:])
        return outname
    elif os.path.exists(outname):
        try: # pdf_viewer.clear() #FixME!
            os.remove(outname)
        except PermissionError as e:
            logger.warn(_("No changes were detected between the two PDFs, but the (old) _diff PDF appears to be open and so cannot be deleted."))
            return 4
    return 0

def pdfimages(infile, dpi=0):
    import gi
    gi.require_version('Poppler', '0.18')
    from gi.repository import Poppler, GLib
    import cairo
    uri = GLib.filename_to_uri(infile, None)
    doc = Poppler.Document.new_from_file(uri, None)
    numpages = doc.get_n_pages()
    if dpi == 0:
        dpi = 3
    else:
        dpi /= 72
    for i in range(numpages):
        page = doc.get_page(i)
        if page is None:
            continue
        w, h = (int(x*dpi) for x in page.get_size())  # in points
        surface = cairo.ImageSurface(cairo.Format.ARGB32, w, h)
        ctx = cairo.Context(surface)
        ctx.scale(dpi, dpi)
        ctx.set_source_rgba(1., 1., 1., 1.)
        ctx.rectangle(0, 0, w, h)
        ctx.fill()
        try:
            page.render(ctx)
            imgr = Image.frombuffer(mode='RGBA', size=(w,h), data=surface.get_data().tobytes())
            b, g, r, a = imgr.split()
            img = Image.merge('RGB', (r, g, b))
        except MemoryError:
            return
        yield img

def main():
    def splithex(s):
        return [int(s[i:i+2], 16) for i in range(0, 6, 2)]

    def doError(txt, secondary=None, **kw):
        print(txt)

    parser = argparse.ArgumentParser()
    parser.add_argument('infilea', help="Original input PDF file")
    parser.add_argument('infileb', help="Different input PDF file")
    parser.add_argument('outfile', help="Output difference PDF file")
    parser.add_argument('-O','--oldcol',help="From colour 6 hex RGB digits")
    parser.add_argument('-N','--newcol',help="To colour 6 hex RGB digits")
    args = parser.parse_args()

    if args.oldcol is not None:
        args.oldcol = splithex(args.oldcol)
    if args.newcol is not None:
        args.newcol = splithex(args.newcol)

    res = createDiff(os.path.abspath(args.infilea), os.path.abspath(args.infileb),
            os.path.abspath(args.outfile), doError, color=args.oldcol, oldcolor=args.newcol)

if __name__ == "__main__":
    ptxprint.pdf.pdfdiff.main()
