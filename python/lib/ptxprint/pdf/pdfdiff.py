import os, re, argparse
from PIL import Image, ImageChops, ImageEnhance, ImageOps, ImageDraw
from ptxprint.utils import _
import logging
logger = logging.getLogger(__name__)

def createDiff(pdfname, othername, outname, doError, color=None, onlydiffs=True, 
                maxdiff=False, oldcolor=None, limit=0, dpi=0, boxmode="auto", offset=0, ignore=(), geometry=None, **kw):
    """ boxmode "auto" compares the TrimBox of each page, so that a PDF with crop marks (whose MediaBox is
        bigger than the page) lines up with one without. Any other value compares what Poppler renders by
        default: the CropBox, which is the MediaBox when there is no CropBox.
        offset pairs page i of pdfname with page i+offset of othername: positive skips that many pages at
        the start of othername (the old PDF), negative skips that many at the start of pdfname.
        ignore is a collection of "topbottom" (headers, footers, page numbers) and "sides" (margin notes,
        thumb tabs). Those parts of the page are blanked in both PDFs before comparing and shaded in the
        result. Where they are comes from geometry, which describes the *new* PDF (pdfname):
            {"top": mm of margin above the text, "bottom": mm below, "sides": columnExtents(parlocs)} """
    if color is None or not len(color):
        color = (240, 0, 0)
    if oldcolor is None or not len(oldcolor):
        oldcolor = (0, 0, 240)
    if not os.path.exists(othername):
        return 2
    try:
        ingen = pdfimages(pdfname, dpi=dpi, boxmode=boxmode, start=max(-offset, 0))
        ogen = pdfimages(othername, dpi=dpi, boxmode=boxmode, start=max(offset, 0))
    except ImportError:
        return 1
    results = []
    hasdiffs = False
    for iimg in ingen:
        oimg = next(ogen, None)
        if oimg is None:
            break
        if abs(oimg.size[0] - iimg.size[0]) > 2 or abs(oimg.size[1] - iimg.size[1]) > 2:
            doError(_("Page sizes differ between output and base. Cannot create a difference."),
                threaded=True, title=_("Difference Error"))
            return 3
        info = iimg.info
        if oimg.size != iimg.size:      # rounding of the trim box to whole pixels
            size = (min(oimg.size[0], iimg.size[0]), min(oimg.size[1], iimg.size[1]))
            oimg = oimg.crop((0, 0) + size)
            iimg = iimg.crop((0, 0) + size)
        zones = zoneRects(info, iimg.size, ignore, geometry)
        if len(zones):
            for im in (oimg, iimg):
                draw = ImageDraw.Draw(im)
                for r in zones:
                    draw.rectangle(r, fill=(255, 255, 255))
        dmask = ImageChops.difference(oimg, iimg).convert("L")
        dval = sum([i * x / 256. for i, x in enumerate(dmask.histogram()) if i > 12])
        logger.debug(f"Difference val = {dval} size({dmask.getbbox()})")
        if not dmask.getbbox() or dval < 2.:
            if onlydiffs:
                continue
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
        if len(zones):
            shade = Image.new("L", nimg.size, 0)
            draw = ImageDraw.Draw(shade)
            for r in zones:
                draw.rectangle(r, fill=90)
            nimg.paste(Image.new("RGB", nimg.size, (120, 120, 120)), (0, 0), shade)
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

def zoneRects(info, size, ignore, geometry):
    """ Pixel rectangles (x0, y0, x1, y1) of a rendered page that are to be ignored. info is the .info of the
        image from pdfimages: the PDF box that was rendered, the pixels per point, and the page index. """
    rects = []
    if not len(ignore) or not geometry or "box" not in info:
        return rects
    w, h = size
    box, scale = info["box"], info["scale"]
    if "topbottom" in ignore:
        top = int(round(float(geometry.get("top", 0)) * 72 / 25.4 * scale))
        bottom = int(round(float(geometry.get("bottom", 0)) * 72 / 25.4 * scale))
        if top > 0:
            rects.append((0, 0, w - 1, min(top, h) - 1))
        if bottom > 0:
            rects.append((0, max(h - bottom, 0), w - 1, h - 1))
    if "sides" in ignore:
        cols = geometry.get("sides", {}).get(info["page"])
        if cols is not None:
            left = int(round((cols[0] - box[0]) * scale))
            right = int(round((cols[1] - box[0]) * scale))
            if left > 0:
                rects.append((0, 0, min(left, w) - 1, h - 1))
            if right < w:
                rects.append((max(right, 0), 0, w - 1, h - 1))
    return rects

def columnExtents(parlocsfile):
    """ Reads the .parlocs file that came with a PDF and returns {page index: (xmin, xmax)}: the horizontal
        extent of the text columns on that page, in PDF points, measured in the page's own coordinates. Pages
        without any text column are missing. The extent allows for mirrored pages, gutters, margin notes
        and so on, because it is where the text was actually put. """
    from ptxprint.parlocs import readpts
    res = {}
    if parlocsfile is None or not os.path.exists(parlocsfile):
        return res
    tobp = 72. / 72.27       # TeX points to PDF points
    page = -1
    with open(parlocsfile, encoding="utf-8") as inf:
        for l in inf:
            m = re.match(r"^\\@(pgstart|colstart|Poly@colstart)\s*\{(.*)\}\s*$", l)
            if m is None:
                continue
            if m.group(1) == "pgstart":
                page += 1
                continue
            p = m.group(2).split("}{")
            if len(p) < 5 or page < 0:
                continue
            x = readpts(p[3]) * tobp
            e = res.get(page, (x, x))
            res[page] = (min(e[0], x), max(e[1], x + readpts(p[2]) * tobp))
    return res

def trimBoxes(infile):
    """ Returns a list, one per page, of the TrimBox [llx, lly, urx, ury] in PDF points, or None for a
        page with no TrimBox (or if the file cannot be read by pdfrw). """
    try:
        from ptxprint.pdfrw import PdfReader
        return [[float(x) for x in p.inheritable.TrimBox] if p.inheritable.TrimBox is not None else None
                for p in PdfReader(infile).pages]
    except Exception as e:
        logger.debug(f"Could not read TrimBoxes from {infile}: {e}")
        return []

def pdfimages(infile, dpi=0, boxmode="auto", start=0):
    import gi
    gi.require_version('Poppler', '0.18')
    from gi.repository import Poppler, GLib
    import cairo
    uri = GLib.filename_to_uri(infile, None)
    doc = Poppler.Document.new_from_file(uri, None)
    numpages = doc.get_n_pages()
    trims = trimBoxes(infile) if boxmode == "auto" else []
    if dpi == 0:
        dpi = 3
    else:
        dpi /= 72
    for i in range(start, numpages):
        page = doc.get_page(i)
        if page is None:
            continue
        w, h = (int(x*dpi) for x in page.get_size())  # in points
        # Poppler draws the CropBox with its top left corner at the origin. Shift so that the TrimBox is
        # what lands on the surface: whatever is outside it (crop marks, bleed) is clipped by the surface.
        shiftx = shifty = 0.
        trim = trims[i] if i < len(trims) else None
        crop = page.get_crop_box()
        box = (crop.x1, crop.y1, crop.x2, crop.y2)
        if trim is not None:
            shiftx = trim[0] - crop.x1
            shifty = crop.y2 - trim[3]
            w, h = (int(round((trim[2] - trim[0]) * dpi)), int(round((trim[3] - trim[1]) * dpi)))
            box = tuple(trim)
        surface = cairo.ImageSurface(cairo.Format.ARGB32, w, h)
        ctx = cairo.Context(surface)
        ctx.set_source_rgba(1., 1., 1., 1.)
        ctx.rectangle(0, 0, w, h)
        ctx.fill()
        ctx.scale(dpi, dpi)
        ctx.translate(-shiftx, -shifty)
        try:
            page.render(ctx)
            imgr = Image.frombuffer(mode='RGBA', size=(w,h), data=surface.get_data().tobytes())
            b, g, r, a = imgr.split()
            img = Image.merge('RGB', (r, g, b))
        except MemoryError:
            return
        img.info.update(box=box, scale=dpi, page=i)
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
    parser.add_argument('-O','--oldcol',help="From colour 6 hex RGB digits. Default: red.")
    parser.add_argument('-N','--newcol',help="To colour 6 hex RGB digits. Default: blue.")
    parser.add_argument('-A','--allpages', action="store_true", help="Show all pages? Default: show only non-identical pages.")
    parser.add_argument('-m','--maxpages', type=int, default=0, help="Maximum pages to show. Default: no maximum")
    args = parser.parse_args()

    if args.oldcol is not None:
        args.oldcol = splithex(args.oldcol)
    if args.newcol is not None:
        args.newcol = splithex(args.newcol)

    res = createDiff(os.path.abspath(args.infilea), os.path.abspath(args.infileb),
            os.path.abspath(args.outfile), doError, color=args.oldcol, oldcolor=args.newcol, onlydiffs=not args.allpages, limit=args.maxpages)

if __name__ == "__main__":
    main()
