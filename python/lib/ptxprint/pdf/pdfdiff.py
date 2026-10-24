import os, re, argparse
from PIL import Image, ImageChops, ImageEnhance, ImageOps, ImageDraw, ImageFilter
from ptxprint.utils import _
import logging
logger = logging.getLogger(__name__)

def createDiff(pdfname, othername, outname, doError, color=None, onlydiffs=True, 
                maxdiff=False, oldcolor=None, limit=0, dpi=0, boxmode="auto", offset=0, ignore=(), geometry=None, smart=False, **kw):
    """ boxmode "auto" compares the TrimBox of each page, so that a PDF with crop marks (whose MediaBox is
        bigger than the page) lines up with one without. Any other value compares what Poppler renders by
        default: the CropBox, which is the MediaBox when there is no CropBox.
        offset pairs page i of pdfname with page i+offset of othername: positive skips that many pages at
        the start of othername (the old PDF), negative skips that many at the start of pdfname.
        ignore is a collection of "topbottom" (headers, footers, page numbers) and "sides" (margin notes,
        thumb tabs). Those parts of the page are blanked in both PDFs before comparing and shaded in the
        result. Where they are comes from geometry, which describes the *new* PDF (pdfname):
            {"top": mm of margin above the text, "bottom": mm below, "sides": columnExtents(parlocs)}
        smart lines up each page of the old PDF with the new one before comparing, so that moving the text
        block on the page (changed margins or gutter) is not reported when the text itself is unchanged. """
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
    compared = 0
    aligner = Aligner() if smart else None
    for iimg, oimg in pagePairs(ingen, ogen):
        compared += 1
        if abs(oimg.size[0] - iimg.size[0]) > 2 or abs(oimg.size[1] - iimg.size[1]) > 2:
            doError(_("Page sizes differ between output and base. Cannot create a difference."),
                threaded=True, title=_("Difference Error"))
            return 3
        info = iimg.info
        if oimg.size != iimg.size:      # rounding of the trim box to whole pixels
            size = (min(oimg.size[0], iimg.size[0]), min(oimg.size[1], iimg.size[1]))
            oimg = oimg.crop((0, 0) + size)
            iimg = iimg.crop((0, 0) + size)
        unmoved = None
        if aligner is not None:
            shift = aligner.shift(oimg, iimg, info.get("page", compared), info.get("scale", 3))
            if shift != (0, 0):
                logger.debug(f"Page {compared}: moving the old page by {shift} to line it up")
                unmoved = (oimg, shift)
                oimg = shiftImage(oimg, *shift)
        zones = zoneRects(info, iimg.size, ignore, geometry)
        if len(zones):
            for im in (oimg, iimg) if unmoved is None else (oimg, iimg, unmoved[0]):
                draw = ImageDraw.Draw(im)
                for r in zones:
                    draw.rectangle(r, fill=(255, 255, 255))
        # What did not move with the text (page numbers, running headers) matches the old page where it was
        dmask, changed = realDifference(oimg, iimg, info.get("scale", 3), alternative=unmoved[0] if unmoved else None,
                                        shift=unmoved[1] if unmoved else (0, 0),
                                        # A moved page has more noise, so it takes a bigger change to count. A
                                        # normal compare notices as little as a comma where a full stop was.
                                        minchanged=45 if unmoved else 14)
        logger.debug(f"Changed pixels = {changed}")
        if not changed:
            if onlydiffs:
                continue
        else:
            hasdiffs = True
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
    if not compared:
        return 5
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

def shiftImage(img, dx, dy, fill=None):
    """ A copy of img moved by dx, dy pixels, with white (or fill) where there was nothing. """
    if fill is None:
        fill = (255, 255, 255) if img.mode == "RGB" else 255
    res = Image.new(img.mode, img.size, fill)
    res.paste(img, (dx, dy))
    return res


def inkProfile(img, axis, factor=1):
    """ How much ink there is in each column (axis 0) or row (axis 1), averaged over groups of factor pixels. """
    grey = img.convert("L")
    w, h = grey.size
    if axis == 0:
        prof = grey.resize((max(w // factor, 1), 1), Image.BOX)
    else:
        prof = grey.resize((1, max(h // factor, 1)), Image.BOX)
    return [255 - v for v in prof.getdata()]


def profileError(old, new, shift):
    """ Mean difference between new and old when old is moved by shift (in profile steps). """
    n = len(old)
    if shift >= n or -shift >= n:
        return None
    if shift >= 0:
        o, nw = old[:n - shift], new[shift:]
    else:
        o, nw = old[-shift:], new[:n + shift]
    return sum(abs(a - b) for a, b in zip(o, nw)) / len(o)


def bestShift(old, new, limit, factor):
    """ The movement of old (in steps of the profile) that makes it most like new, within limit steps. """
    best, besterr = 0, None
    for s in range(-limit, limit + 1):
        err = profileError(old, new, s)
        if err is not None and (besterr is None or err < besterr):
            best, besterr = s, err
    return best


class Aligner:
    """ Works out how far the text on a page has moved between two PDFs. Changing the margins or adding a
        gutter moves the whole text block without changing it, and (with facing pages) it moves opposite ways
        on left and right pages. So the movement is worked out for each page, from the ink in each column and
        row. A page with hardly any ink gives no clue, so it takes what the last page of the same sort needed. """
    maxmm = 30          # the furthest the text block is expected to have moved
    minink = 0.5        # average darkness below which a page is taken to be empty

    def __init__(self):
        self.last = {}

    def shift(self, oimg, iimg, page, scale=3):
        parity = page % 2
        px = int(round(self.maxmm / 25.4 * 72 * scale))
        res = []
        for axis in (0, 1):
            # coarse, on a blurred profile, then fine on the real one
            coarse = 3
            o3, n3 = inkProfile(oimg, axis, coarse), inkProfile(iimg, axis, coarse)
            if sum(n3) / len(n3) < self.minink or sum(o3) / len(o3) < self.minink:
                self.last.setdefault(parity, [0, 0])
                return tuple(self.last[parity])
            s = bestShift(o3, n3, px // coarse, coarse) * coarse
            o1, n1 = inkProfile(oimg, axis), inkProfile(iimg, axis)
            lo = [s + k for k in range(-coarse, coarse + 1)]
            errs = [(profileError(o1, n1, t), t) for t in lo]
            errs = [e for e in errs if e[0] is not None]
            err0 = profileError(o1, n1, 0)
            best = min(errs)[1] if len(errs) else 0
            # only move the page if that is clearly better than leaving it where it is
            if err0 is not None and len(errs) and min(errs)[0] > 0.6 * err0:
                best = 0
            res.append(best)
        self.last[parity] = res
        return tuple(res)


def pagePairs(ingen, ogen):
    """ Pairs up the pages of the new and old PDFs. A page that only one of them has is paired with a blank page,
        so that the extra pages show up as differences instead of being silently left out. """
    first = True
    while True:
        iimg = next(ingen, None)
        oimg = next(ogen, None)
        if iimg is None and oimg is None:
            return
        if first and (iimg is None or oimg is None):
            return          # one has no pages at all (e.g. the offset is past its end): nothing to pair
        first = False
        if oimg is None:
            oimg = Image.new("RGB", iimg.size, (255, 255, 255))
        elif iimg is None:
            iimg = Image.new("RGB", oimg.size, (255, 255, 255))
        yield iimg, oimg


def realDifference(oimg, iimg, scale=3, alternative=None, shift=(0, 0), minchanged=14):
    """ Returns (mask, changed) where mask marks the parts of the page that really differ and changed says
        whether there are enough of them to count. Two renderings of the same text rarely agree to the
        pixel: glyphs and marks land on slightly different fractions of a pixel (e.g. when the page sits at
        a different offset in the PDF, as with crop marks). So a pixel only differs if one page has ink
        with no ink within a pixel or so of it on the other, and a few such pixels are not a change.
        alternative is the old page before it was moved to line up with the new one. """
    radius = max(1, int(round(scale / 3.)))
    size = 2 * radius + 1
    il = iimg.convert("L")

    def rawMasks(old):
        ol = old.convert("L")
        added = ImageChops.subtract(ol.filter(ImageFilter.MinFilter(size)), il)     # ink in new, none near it in old
        removed = ImageChops.subtract(il.filter(ImageFilter.MinFilter(size)), ol)   # ink in old, none near it in new
        return added.point(lambda x: 255 if x > 40 else 0), removed.point(lambda x: 255 if x > 40 else 0)

    added, removed = rawMasks(oimg)
    if alternative is not None:
        # The old page was moved to line it up. Things that did not move with the text (page numbers, running
        # headers) match the old page where it was, so they are not differences. New ink needs to be new
        # either way; old ink needs to be unmatched where it was, which is where it was before it was moved.
        altadded, altremoved = rawMasks(alternative)
        added = ImageChops.darker(added, altadded)
        removed = ImageChops.darker(removed, shiftImage(altremoved, shift[0], shift[1], fill=0))
    mask = ImageChops.lighter(added, removed)
    changed = mask.histogram()[255]
    if changed < minchanged * (radius ** 2):
        return mask, 0
    return mask.filter(ImageFilter.MaxFilter(5)), changed


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
