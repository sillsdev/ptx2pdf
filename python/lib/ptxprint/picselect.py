import gi
import os
import re
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import zipfile, appdirs, json
import logging

logger = logging.getLogger(__name__)

from ptxprint.utils import _, extraDataDir
from ptxprint.reference import RefList

def unpackImageset(filename, prjdir):
    with zipfile.ZipFile(filename) as zf:
        if "illustrations.json" in zf.namelist():
            with zf.open("illustrations.json") as zill:
                zdat = json.load(zill)
            dirname = zdat.get('id', "Unknown")
            uddir = extraDataDir("imagesets", dirname, create=True)
        else:
            # Check if the ZIP file contains any image files
            contains_images = any(is_image_file(name) for name in zf.namelist())
            if not contains_images:
                return None
            uddir = os.path.join(prjdir,"local","figures")
            os.makedirs(uddir, exist_ok=True)
            dirname = ""
        if uddir is None:
            return None
        zf.extractall(path=uddir)
    return dirname

def is_image_file(filename):
    image_extensions = {'.jpg', '.jpeg', '.tif', '.tiff', '.png', '.gif', '.bmp'}
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def getImageSets():
    uddir = os.path.join(appdirs.user_data_dir("ptxprint", "SIL"), "imagesets")
    if os.path.exists(uddir):
        return sorted([f for f in os.listdir(uddir) if os.path.isdir(os.path.join(uddir, f))])
    else:
        return None

def fill_me(parent, fpath, size):
    thumbnail_image = Gtk.Image()
    thumbnail_image.set_hexpand(True)
    thumbnail_image.set_vexpand(True)

    # Load the original image
    original_pixbuf = GdkPixbuf.Pixbuf.new_from_file(fpath)

    # Calculate the thumbnail size while preserving the aspect ratio
    width = original_pixbuf.get_width()
    height = original_pixbuf.get_height()
    aspect_ratio = width / height

    if width > height:
        thumbnail_width = size
        thumbnail_height = int(thumbnail_width / aspect_ratio)
    else:
        thumbnail_height = size
        thumbnail_width = int(thumbnail_height * aspect_ratio)

    # Scale the original image to the calculated thumbnail size
    # print(f"{fpath} {thumbnail_width} x {thumbnail_height} from {width} x {height} @ {size}")
    thumbnail_pixbuf = original_pixbuf.scale_simple(thumbnail_width, thumbnail_height, GdkPixbuf.InterpType.BILINEAR)
    thumbnail_image.set_from_pixbuf(thumbnail_pixbuf)
    parent.set_image(thumbnail_image)
    parent.show()


class ThumbnailDialog:
    def __init__(self, dlg, view, gridbox, gridcols):
        self.dlg = dlg
        self.view = view
        self.artists = set()
        self.reflist = []
        self.filters = set()
        self.imageset = None
        self.grid = gridbox
        self.gridcols = gridcols
        self.imagedata = None
        self.langdata = None
        self.tilesize = 100
        self.selected_thumbnails = set()
        self.reftext = None

    def run(self):
        uddir = os.path.join(appdirs.user_data_dir("ptxprint", "SIL"), "imagesets")
        if not os.path.exists(uddir):
            self.view.onImageSetClicked(None)

        logger.debug("Starting to load images")
        ltv = self.view.builder.get_object("ls_artists")
        for r in ltv:
            if r[0]:
                self.artists.add(r[1].lower())
            else:
                self.artists.discard(r[1].lower())
        imgset = self.view.get('ecb_artPictureSet')
        if not imgset:
            imagesets = getImageSets()
            if imagesets is None or not len(imagesets):
                return None
            else:
                imgset = imagesets[0]
        else:
            self.view.getBooks()
            reflist = self.view.bookrefs
            logger.debug(f"Start with bookrefs: {reflist}")
            self.view.set('t_artRefRange', str(reflist))
        self.set_imageset(imgset)
        response = self.dlg.run()
        self.dlg.hide()
        if response == Gtk.ResponseType.OK:
            return self.selected_thumbnails
        else:
            return None

    def set_imageset(self, s):
        self.imageset = s
        imagesetdir = extraDataDir("imagesets", self.imageset)
        if imagesetdir is None:
            return
        illpath = os.path.join(imagesetdir, "illustrations.json")
        if os.path.exists(illpath):
            with open(illpath, encoding="utf-8") as inf:
                self.imagedata = json.load(inf)
        else:
            self.imagedata = None
        # fill in list of artists
        model = self.view.builder.get_object("ls_artists")
        model.clear()
        for a in sorted(self.imagedata['sets']):
            name = self.view.copyrightInfo['copyrights'].get(a.lower(), {}).get('artist', _("Unknown"))
            model.append([False, a.upper(), name])
        self.artists.clear()
        langpath = os.path.join(imagesetdir, "lang_{}.json".format(self.view.lang.lower()))
        if not os.path.exists(langpath):
            langpath = os.path.join(imagesetdir, "lang_en.json")
        if os.path.exists(langpath):
            with open(langpath, encoding="utf-8") as inf:
                self.langdata = json.load(inf)
        else:
            self.langdata = None
        self.setup_tiles()
        self.refresh()

    def setup_tiles(self):
        imagesetdir = extraDataDir("imagesets", self.imageset)
        imagesdir = os.path.join(imagesetdir, "images")
        if not os.path.exists(imagesdir):
            return
        for c in self.grid.get_children():
            self.grid.remove(c)
        self.image_tiles = {}
        for imagefile in os.listdir(imagesdir):
            (imageid, imageext) = os.path.splitext(imagefile)
            if not imageext.lower() in (".jpg", ".tif"):
                continue
            w = Gtk.ToggleButton()
            w.connect("toggled", self.on_thumbnail_toggled, imageid)
            w.connect("enter-notify-event", self.on_thumbnail_entered, imageid)
            self.image_tiles[imageid] = (w, False, os.path.join(imagesdir, imagefile))
        logger.debug(f"tiles set up for {self.imageset}")

    def add_artist(self, artid):
        self.artists.add(artid.lower())
        self.refresh()

    def remove_artist(self, artid):
        self.artists.discard(artid.lower())
        self.refresh()

    def set_filter(self, s):
        self.filters = set(c.lower() for c in s.split())
        self.enable_refresh()

    def test_filter(self, imgid, filters):
        if self.langdata is None:
            return True
        if any(x in filters for x in self.langdata.get(imgid, {}).get('kwds', [])):
            return True
        if any(x.lower() in filters for x in self.langdata.get(imgid, {}).get('title', '').split()):
            return True
        return False

    def set_reflist(self, s):
        self.reftext = s
        self.enable_refresh()

    def update_reflist(self):
        if self.reftext is not None and len(self.reftext):
            self.reflist = RefList.fromStr(self.reftext)
        else:
            self.reflist = []
        # logger.debug(f"reflist from {s} to {self.reflist}")

    def get_refs(self, imgid, default=[]):
        if self.imagedata is None:
            return default
        # logger.debug(f"{imgid}: {self.imagedata['images'].get(imgid,{}).get('refs')}")
        return [RefList.fromStr(r)[0] for r in self.imagedata['images'].get(imgid, {}).get('refs', [])]

    def get_imgdir(self):
        imagesetdir = extraDataDir("imagesets", self.imageset)
        if imagesetdir is None:
            return None
        imagesdir = os.path.join(imagesetdir, "images")
        return imagesdir

    def enable_refresh(self):
        b = self.view.builder.get_object("btn_imgRefresh").set_sensitive(True)

    def disable_refresh(self):
        b = self.view.builder.get_object("btn_imgRefresh").set_sensitive(False)

    def refresh(self):
        self.update_reflist()
        self.fill()

    def clear(self):
        for image_tuple in self.image_tiles.values():
            toggle_button = image_tuple[0]
            toggle_button.set_active(False)
        self.selected_thumbnails = set()
        status = "(0 images selected)"
        self.view.set("l_artStatusLine", status)

    def fill(self):
        imagesdir = self.get_imgdir()
        if imagesdir is None:
            return
        imageids = set()
        self.imgrefs = {}
        for imagefile in os.listdir(imagesdir):
            (imageid, imageext) = os.path.splitext(imagefile)
            if not imageext.lower() in (".jpg", ".tif"):
                continue
            if len(self.artists) and imageid[:2].lower() not in self.artists:
                continue
            if len(self.filters) and not self.test_filter(imageid, self.filters):
                continue
            if len(self.reflist):
                refs = self.get_refs(imageid)
                if not len(refs):
                    continue
                for r in refs:
                    if r in self.reflist:
                        # logger.debug(f"Testing {imageid}: {refs}, {r} in {self.reflist}")
                        self.imgrefs[imageid] = r
                        break
                else:
                    continue
            imageids.add(imageid)
        self.set_images(imagesdir, sorted(imageids))
        self.disable_refresh()

    def imgkey(self, imgid, mode="ref"):
        if mode == "pop":
            pop = self.imagedata['images'].get(imgid, {}).get('pop', 0)
        else:
            pop = 0
        res = self.imgrefs[imgid].astag() if imgid in self.imgrefs else "zzzz"+imgid
        return (pop, res)

    def set_images(self, fbase, imageids):
        # logger.debug(f"Setting up for images: {imageids}")
        #children = sorted(self.grid.get_children(),
        #        key = lambda c:(self.grid.child_get_property(c, "top_attach"), self.grid.child_get_property(c, "left-attach")))
        for c in self.grid.get_children():
            c.hide()
            self.grid.remove(c)
        sortby = self.view.get('r_imgSort')
        images = sorted(imageids, key=lambda s:self.imgkey(s, mode=sortby))
        logger.debug(f"Setting up grid for {images}")
        for i, imgid in enumerate(images):
            w, isLoaded, fpath = self.image_tiles[imgid]
            if not isLoaded:
                fill_me(w, fpath, self.tilesize)
                self.image_tiles[imgid] = (w, True, fpath)
            self.grid.attach(w, i % self.gridcols, i // self.gridcols, 1, 1)
            w.show()
        self.grid.queue_resize()
        logger.debug(f"Image grid complete")

    def on_thumbnail_toggled(self, button, imageid):
        bibrefs = self.get_refs(imageid, default=[None])
        bibref = bibrefs[0] if len(bibrefs) else None
        val = (imageid, bibref, self.langdata.get(imageid, {}).get("title", ""))

        if button.get_active():
            self.selected_thumbnails.add(val)
        else:
            self.selected_thumbnails.discard(val)
        status = ", ".join(x[0] for x in sorted(self.selected_thumbnails, key=lambda t:(t[1], t[0]))) + f" ({len(self.selected_thumbnails)} images selected)"
        self.view.set("l_artStatusLine", status)

    def on_thumbnail_entered(self, button, event, imageid):
        cinfo = self.view.copyrightInfo
        artist = cinfo['copyrights'].get(imageid[:2].lower(), {}).get('artist', '')
        if len(artist):
            self.view.set("l_imgIDArtist", "{}, {}".format(imageid, artist))
        else:
            self.view.set("l_imgIDArtist", imageid)
        if self.langdata:
            desc = self.langdata.get(imageid, {}).get("title", "")
            self.view.set("l_imgDesc", desc if len(desc) else "")
            kwds = ", ".join(self.langdata.get(imageid, {}).get("kwds", []))
            self.view.set('l_imgKeywords', kwds if len(kwds) else "")
        else:
            self.view.set("l_imgDesc", "")
            self.view.set('l_imgKeywords', "")

        if self.imagedata:
            refs = "; ".join(self.imagedata["images"].get(imageid, {}).get('refs', []))
            refs = re.sub(":0", "", refs)
            self.view.set('l_imgRefs', refs if len(refs) else "")
        else:
            self.view.set('l_imgRefs', "")
