#!/usr/bin/python3

from PIL import Image, ImageCms
from ptxprint.pdfrw.uncompress import uncompress
from ptxprint.pdfrw.compress import compress
from ptxprint.pdfrw.objects import PdfDict, PdfName
import numpy as np
import io

# Thanks to Divakar: https://stackoverflow.com/questions/38055065/efficient-way-to-convert-image-stored-as-numpy-array-into-hsv
def rgb_vecto_hsv(img):
    """Input is ndarray.shape(y, x, 3)"""
    maxc = img.max(-1)
    minc = img.min(-1)

    out = np.zeros(img.shape)
    out[:,:,2] = maxc
    out[:,:,1] = (maxc-minc) / (maxc + .0001)

    divs = (maxc[...,None] - img) / ((maxc-minc + .0001)[...,None])
    cond1 = divs[...,2] - divs[...,1]
    cond2 = 2.0 + divs[...,0] - divs[...,2]
    h = 4.0 + divs[...,1] - divs[...,0]
    h[img[...,0] == maxc] = cond1[img[...,0] == maxc]
    h[img[...,1] == maxc] = cond2[img[...,1] == maxc]
    out[:,:,0] = (h / 6.0) % 1.0

    out[minc == maxc,:2] = 0
    return out

def cmyk_vecto_rgb(img):
    out = np.zeros((img.shape[0], img.shape[1], 3))
    k = 1. - img[...,3]
    out[...,0] = (1. - img[...,0]) * k
    out[...,1] = (1. - img[...,1]) * k
    out[...,2] = (1. - img[...,2]) * k
    return out


def DCTDecode(dat):
    return Image.open(io.BytesIO(dat.encode("Latin-1")))

img_modes = {'/DeviceRGB':  'RGB',  '/DefaultRGB':  'RGB',
             '/DeviceCMYK': 'CMYK', '/DefaultCMYK': 'CMYK',
             '/DeviceGray': 'L',    '/DefaultGray': 'L',
             '/Indexed':    'P'}

class PDFImage:

    def __init__(self, xobj, compressor=None):
        self.spotb = None
        self.spotc = None
        self.compressor = compressor or compress
        self.colorspace = xobj['/ColorSpace'] if '/ColorSpace' in xobj else None
        if self.colorspace[0] == "/ICCBased":
            uncompress([self.colorspace[1]])
            self.icc = ImageCms.ImageCmsProfile(io.BytesIO(self.colorspace[1].stream.encode("Latin-1")))
            compress([self.colorspace[1]])
        self.height = xobj['/Height']
        self.width = xobj['/Width']
        self.filt = xobj['/Filter']
        self.bits = xobj['/BitsPerComponent']
        if self.filt in ("/DCTDecode", "/JPXDecode"):
            self.img = DCTDecode(xobj.stream)
        elif self.filt == "/FlateDecode":
            uncompress([xobj])
            if self.colorspace[0] == "/Indexed":
                cs, base, hival, lookup = self.colorspace
            mode = img_modes[cs]
            self.img = Image.frombytes(mode, (self.width, self.height), xobj.stream.encode("Latin-1"))
            if cs == "/Indexed":
                img.putpalette(lookup)
        elif self.filt == "/CCITTFaxDecode":
            print("No CCITTFaxDecode support yet")
            self.img = None
    
    def asXobj(self):
        res = PdfDict()
        res[PdfName("Height")] = self.height
        res[PdfName("Width")] = self.width
        res[PdfName("Subtype")] = PdfName("Image")
        res[PdfName("Type")] = PdfName("XObject")
        res[PdfName("ColorSpace")] = self.colorspace
        res[PdfName("BitsPerComponent")] = self.bits
        if self.spotc is None:
            if self.spotb is not None:
                self.img = Image.fromarray((self.spotb * 255).astype(np.uint8), "L")
            stream = io.BytesIO()
            self.img.save(stream, 'JPEG')
            res.stream = stream.getvalue().decode("Latin-1")
            res[PdfName("Filter")] = PdfName("DCTDecode")
        else:
            spotb = (self.spotb * 255).astype(np.uint8).tobytes()
            spotc = (self.spotc * 255).astype(np.uint8).tobytes()
            res.stream = b"".join("".join(*z) for z in zip(spotb, spotc))
            res.Binary = True
            #self.compressor([res])
        return res

    def analyse(self, hue, hrange):
        img = np.asarray(self.img) / 255.
        if img.shape[-1] == 4:
            img = cmyk_vecto_rgb(img)
        hsv = rgb_vecto_hsv(img)
        incolor = hsv[np.isclose(hsv[:,:,0], hue, atol=hrange)]
        if not len(incolor):
            return None
        maxs = hsv[:,:,1].max()
        maxv = hsv[:,:,2].max()
        return (maxs, maxv)

    def duotone(self, hsv, hrange, spotcspace=None, blackcspace=None):
        img = np.asarray(self.img) / 255.
        if img.shape[-1] == 4:
            img = cmyk_vecto_rgb(img)
        hsvimg = rgb_vecto_hsv(img)
        # calculate as if all in the hsv colour range
        spotb = (1 - hsv[2]) - (1 - hsvimg[:,:,2])
        # replace out of range colours with grey
        m = np.logical_not(np.isclose(hsvimg[...,0], hsv[0], hrange))
        if np.all(m):
            self.spotb = hsvimg[...,2]
            self.spotc = None
            self.colorspace = blackcspace
            return False
        else:
            spotb[m] = hsvimg[m, 2]  # black volume
            spotv = hsvimg[:,:,1] / hsv[1]
            spotv[m] = 0.
            self.spotc = spotv
            self.spotb = spotb
            self.colorspace = spotcspace
        return True
        
        
if __name__ == "__main__":
    import argparse, sys, os

    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from ptxprint.pdfrw import PdfReader, PdfWriter

    parser = argparse.ArgumentParser()
    parser.add_argument("infile",help="Input PDF")
    parser.add_argument("outfile",help="Output PDF")
    args = parser.parse_args()

    trailer = PdfReader(args.infile)        
    for pagenum, page in enumerate(trailer.pages, 1):
        r = page.Resources
        if r is None:
            continue
        xobjs = r.XObject
        if xobjs is None:
            continue
        for x, xo in list(xobjs.items()):
            img = PDFImage(xo)
            xobjs[x] = img.asXobj()
    w = PdfWriter(args.outfile, trailer=trailer, version='1.4', compress=True, do_compress=compress)
    w.write()
