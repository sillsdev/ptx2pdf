import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import zipfile, appdirs, json
import logging

logger = logging.getLogger(__name__)

from ptxprint.utils import extraDataDir
from ptxprint.reference import RefList

def unpackImageset(dirname, filename):
    uddir = extraDataDir("imagesets", dirname, create=True)
    if uddir is None:
        return False
    with zipfile.ZipFile(filename) as zf:
        zf.extractall(path=uddir)
    return True

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

    def run(self):
        uddir = os.path.join(appdirs.user_data_dir("ptxprint", "SIL"), "imagesets")
        if not os.path.exists(uddir):
            self.view.onImageSetClicked(None)

        logger.debug("Starting to load images")
        self.view.getBooks()
        reflist = self.view.bookrefs
        logger.debug(f"Start with bookrefs: {reflist}")
        self.view.set('t_artRefRange', str(reflist))
        ltv = self.view.builder.get_object("ls_artists")
        for r in ltv:
            if r[0]:
                self.artists.add(r[1].lower())
            else:
                self.artists.discard(r[1].lower())
        imagesets = getImageSets()
        if len(imagesets):
            self.set_imageset(imagesets[0])
        self.fill()
        response = self.dlg.run()
        self.dlg.hide()
        if response == Gtk.ResponseType.OK:
            return self.thumbnails.selected_thumbnails
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
        langpath = os.path.join(imagesetdir, "lang_{}.json".format(self.view.lang.lower()))
        print(langpath)
        if not os.path.exists(langpath):
            langpath = os.path.join(imagesetdir, "lang_en.json")
        if os.path.exists(langpath):
            with open(langpath, encoding="utf-8") as inf:
                self.langdata = json.load(inf)
        else:
            self.langdata = None
        self.setup_tiles()

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
        self.fill()

    def remove_artist(self, artid):
        self.artists.discard(artid.lower())
        self.fill()

    def set_filter(self, s):
        self.filters = set(c.lower() for c in s.split())

    def test_filter(self, imgid, filters):
        if self.langdata is None:
            return True
        if any(x in filters for x in self.langdata.get(imgid, {}).get('kwds', [])):
            return True
        if any(x.lower() in filters for x in self.langdata.get(imgid, {}).get('title', '').split()):
            return True
        return False

    def set_reflist(self, s):
        if s is not None and len(s):
            self.reflist = RefList.fromStr(s)
        else:
            self.reflist = []
        # logger.debug(f"reflist from {s} to {self.reflist}")

    def get_refs(self, imgid):
        if self.imagedata is None:
            return []
        # logger.debug(f"{imgid}: {self.imagedata['images'].get(imgid,{}).get('refs')}")
        return [RefList.fromStr(r)[0] for r in self.imagedata['images'].get(imgid, {}).get('refs', [])]

    def get_imgdir(self):
        imagesetdir = extraDataDir("imagesets", self.imageset)
        if imagesetdir is None:
            return
        imagesdir = os.path.join(imagesetdir, "images")
        return imagesdir

    def refresh(self):
        self.fill()

    def fill(self):
        imagesdir = self.get_imgdir()
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
            refs = self.get_refs(imageid)
            if len(self.reflist) and len(refs):
                for r in refs:
                    if r in self.reflist:
                        # logger.debug(f"Testing {imageid}: {refs}, {r} in {self.reflist}")
                        self.imgrefs[imageid] = r
                        break
                else:
                    continue
            imageids.add(imageid)
        self.set_images(imagesdir, sorted(imageids))

    def imgkey(self, imgid):
        res = self.imgrefs[imgid].astag() if imgid in self.imgrefs else "zzzz"+imgid
        # logger.debug(f"{imgid}: {res}")
        return res

    def set_images(self, fbase, imageids):
        # logger.debug(f"Setting up for images: {imageids}")
        #children = sorted(self.grid.get_children(),
        #        key = lambda c:(self.grid.child_get_property(c, "top_attach"), self.grid.child_get_property(c, "left-attach")))
        logger.debug(f"Setting up grid for {len(imageids)}")
        for c in self.grid.get_children():
            c.hide()
            self.grid.remove(c)
        for i, imgid in enumerate(sorted(imageids, key=lambda s:self.imgkey(s))):
            w, isLoaded, fpath = self.image_tiles[imgid]
            if not isLoaded:
                fill_me(w, fpath, self.tilesize)
                self.image_tiles[imgid] = (w, True, fpath)
            self.grid.attach(w, i % self.gridcols, i // self.gridcols, 1, 1)
            w.show()
        self.grid.queue_resize()
        logger.debug(f"Image grid complete")

    def on_thumbnail_toggled(self, button, imageid):
        val = (imageid, self.imgrefs[imageid])
        if button.get_active():
            self.selected_thumbnails.add(val)
        else:
            self.selected_thumbnails.discard(val)

    def on_thumbnail_entered(self, button, event, imageid):
        cinfo = self.view.copyrightInfo
        artist = cinfo['copyrights'].get(imageid[:2].lower(), {}).get('artist', '')
        if len(artist):
            self.view.set("l_imgIDArtist", "{}, {}".format(imageid, artist))
        else:
            self.view.set("l_imgIDArtist", imageid)
        if self.langdata:
            desc = self.langdata.get(imageid, {}).get("title", "")
            if len(desc):
                self.view.set("l_imgDesc", desc)
            kwds = ", ".join(self.langdata.get(imageid, {}).get("kwds", []))
            if len(kwds):
                self.view.set('l_imgKeywords', kwds)
        if self.imagedata:
            refs = "; ".join(self.imagedata["images"].get(imageid, {}).get('refs', []))
            if len(refs):
                self.view.set('l_imgRefs', refs)
