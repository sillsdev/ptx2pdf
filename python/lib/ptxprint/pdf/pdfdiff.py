
import os
from PIL import Image, ImageChops, ImageEnhance, ImageOps
from ptxprint.utils import _

def createDiff(pdfname, othername, outname, doError, color=None, onlydiffs=True, maxdiff=False, oldcolor=None):
    if color is None:
        color = (240, 0, 0)
    if oldcolor is None:
        oldcolor = (0, 0, 240)
    if not os.path.exists(othername):
        return 2
    try:
        ingen = pdfimages(pdfname)
        ogen = pdfimages(othername)
    except ImportError:
        return 1
    results = []
    hasdiffs = False
    for iimg in ingen:
        oimg = next(ogen, None)
        if oimg is None:
            break
        dmask = ImageChops.difference(oimg, iimg).convert("L")
        if not dmask.getbbox():
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
    if hasdiffs and len(results):
        results[0].save(outname, format="PDF", save_all=True, append_images=results[1:])
        return outname
    elif os.path.exists(outname):
        try:
            os.remove(outname)
        except PermissionError as e:
            doError(_("No changes were detected between the two PDFs, but the (old) _diff PDF appears to be open and so cannot be deleted."),
                                 title=_("{} could not be deleted").format(outname), secondary=str(e), threaded=True)
            return 4
    return 0

def pdfimages(infile):
    import gi
    gi.require_version('Poppler', '0.18')
    from gi.repository import Poppler, GLib
    import cairo
    uri = GLib.filename_to_uri(infile, None)
    doc = Poppler.Document.new_from_file(uri, None)
    numpages = doc.get_n_pages()
    for i in range(numpages):
        page = doc.get_page(i)
        w, h = (int(x*3) for x in page.get_size())
        surface = cairo.ImageSurface(cairo.Format.ARGB32, w, h)
        ctx = cairo.Context(surface)
        ctx.scale(3., 3.)
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

