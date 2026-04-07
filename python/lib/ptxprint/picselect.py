import gi
import os
import re
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import zipfile, json
import logging

logger = logging.getLogger(__name__)

from ptxprint.utils import _, extraDataDir, appdirs, allbooks, chaps
from usfmtc.reference import RefList, Ref
from functools import reduce

startchaps = list(zip([b for b in allbooks if 0 < int(chaps[b]) < 999],
                      reduce(lambda a,x: a + [a[-1]+x], (int(chaps[b]) for b in allbooks if 0 < int(chaps[b]) < 999), [0])))
startchaps += [("special", startchaps[-1][1]+1)]
startbooks = dict(startchaps)

class TagableRef(Ref):

    subversecodes = "!@#$%^&*()"
    b64codes = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz|~"
    b64lkup = {b:i for i, b in enumerate(b64codes)}

    def astag(self):
        subverse = ""
        if self.subverse:
            subind = ord(self.subverse) - 0x61
            if subind < 10:
                subverse = self.subversecodes[subind]
        if self.book == "PSA" and self.chapter == 119 and self.verse > 126:
            c = startbooks["special"] + 1
            v = self.verse - 126
        else:
            c = startbooks[self.book] + self.chapter
            v = min(self.verse, 127)
        vals = [(c >> 5) & 63, ((v & 64) >> 6) + ((c & 31) << 1), v & 63]
        return subverse + "".join(self.b64codes[v] for v in vals)

    def asint(self, chapshift=1):
        if self.vrs is None:
            self.loadvrs()
        coffset = self.vrs[books[self.book]][self.chap-1] + (self.chap - 1) * chapshift if self.chap > 1 else 0
        return self.vrs[books[self.book]][0] + coffset + self.verse

    def numverses(self):
        if self.verse is not None:
            return 1
        vrs = self.first.versification or Ref.loadversification()
        if self.chapter is None:
            firstc = 0
            lastc = len(vrs.vnums[self.book])
        else:
            firstc = self.chapter
            lastc = self.chapter + 1
        return vrs.vnums[self.book][lastc] - vrs.vnums[self.book][firstc]


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
        self._idleLoadId = None
        self.dlg.connect("key-press-event", self._onDialogKeyPress)

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
        if 'sets' in self.imagedata:
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
            w.connect("button-press-event", self._onThumbnailRightClicked, imageid)
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
            try:
                self.reflist = RefList(self.reftext, factory=TagableRef)
            except SyntaxError as e:
                self.view.doError(_("References must only use 3 letter book codes, etc."), str(e))
                self.reflist = []
        else:
            self.reflist = []
        # logger.debug(f"reflist from {s} to {self.reflist}")

    def get_refs(self, imgid, default=[]):
        if self.imagedata is None:
            return default
        # logger.debug(f"{imgid}: {self.imagedata['images'].get(imgid,{}).get('refs')}")
        return [RefList(r, factory=TagableRef)[0] for r in self.imagedata['images'].get(imgid, {}).get('refs', [])]

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

    def _setLabelRowVisible(self, header_id, value_id, visible):
        self.view.builder.get_object(header_id).set_visible(visible)
        self.view.builder.get_object(value_id).set_visible(visible)

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

    def _build_imageids(self, imagesdir):
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
                        self.imgrefs[imageid] = r
                        break
                else:
                    continue
            imageids.add(imageid)
        return imageids

    def fill(self):
        imagesdir = self.get_imgdir()
        if imagesdir is None:
            return
        imageids = self._build_imageids(imagesdir)
        if not imageids and self.reflist:
            self.reflist = []
            self.reftext = ""
            self.view.set('t_artRefRange', '')
            imageids = self._build_imageids(imagesdir)
        if not imageids and self.filters:
            self.filters = set()
            self.view.set('t_artSearch', '')
            imageids = self._build_imageids(imagesdir)
        self.set_images(imagesdir, sorted(imageids))
        self.disable_refresh()

    def imgkey(self, imgid, mode="ref"):
        if mode == "pop":
            pop = self.imagedata['images'].get(imgid, {}).get('pop', 0)
        else:
            pop = 0
        res = self.imgrefs[imgid].astag() if imgid in self.imgrefs else "zzzz"+imgid
        return (pop, res)

    _INITIAL_LOAD = 30

    def set_images(self, fbase, imageids):
        # Cancel any in-progress idle load
        if self._idleLoadId is not None:
            GLib.source_remove(self._idleLoadId)
            self._idleLoadId = None

        for c in self.grid.get_children():
            c.hide()
            self.grid.remove(c)

        sortby = self.view.get('r_imgSort')
        images = sorted(imageids, key=lambda s: self.imgkey(s, mode=sortby))
        total_showing = len(images)
        total_all = len(self.image_tiles)

        # Load the first batch synchronously so the dialog opens with images visible
        initial = images[:self._INITIAL_LOAD]
        deferred = images[self._INITIAL_LOAD:]

        for i, imgid in enumerate(initial):
            w, isLoaded, fpath = self.image_tiles[imgid]
            if not isLoaded:
                fill_me(w, fpath, self.tilesize)
                self.image_tiles[imgid] = (w, True, fpath)
            self.grid.attach(w, i % self.gridcols, i // self.gridcols, 1, 1)
            w.show()
        self.grid.queue_resize()

        self._loadQueue = [(imgid, i + self._INITIAL_LOAD) for i, imgid in enumerate(deferred)]
        self._loadTotal = total_showing
        self._loadTotalAll = total_all
        self._loadLoaded = len(initial)

        if self._loadQueue:
            self._updateLoadCount(loading=True)
            self._idleLoadId = GLib.idle_add(self._idleLoadNext)
        else:
            self._updateLoadCount(loading=False)

    def _idleLoadNext(self):
        if not self._loadQueue:
            self._idleLoadId = None
            self._updateLoadCount(loading=False)
            return False

        imgid, pos = self._loadQueue.pop(0)
        w, isLoaded, fpath = self.image_tiles[imgid]
        if not isLoaded:
            fill_me(w, fpath, self.tilesize)
            self.image_tiles[imgid] = (w, True, fpath)
        self.grid.attach(w, pos % self.gridcols, pos // self.gridcols, 1, 1)
        w.show()
        self._loadLoaded += 1

        if not self._loadQueue:
            self._idleLoadId = None
            self._updateLoadCount(loading=False)
            return False

        self._updateLoadCount(loading=True)
        return True

    def _updateLoadCount(self, loading=False):
        if loading:
            msg = _("Loading {} / {}…".format(self._loadLoaded, self._loadTotal))
        elif self._loadTotal == self._loadTotalAll:
            msg = _("Showing all {} images".format(self._loadTotal))
        else:
            msg = _("Showing {} / {} images".format(self._loadTotal, self._loadTotalAll))
        self.view.set('l_imgLoadCount', msg)

    _PREVIEW_SIZE = 400

    def _onDialogKeyPress(self, _, event):
        if (event.keyval == Gdk.KEY_Escape
                and hasattr(self, '_previewPopover')
                and self._previewPopover.get_visible()):
            self._previewPopover.hide()
            return True  # consume — prevent dialog from closing
        return False

    def _setupPreviewPopover(self):
        css = Gtk.CssProvider()
        css.load_from_data(b"""
            popover.imgpreview-popover {
                background-color: #808080;
                border-radius: 4px;
            }
            popover.imgpreview-popover label {
                color: #f0f0f0;
            }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self._previewPopover = Gtk.Popover()
        self._previewPopover.set_position(Gtk.PositionType.RIGHT)
        self._previewPopover.get_style_context().add_class("imgpreview-popover")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_start(8)
        box.set_margin_end(8)
        box.set_margin_top(8)
        box.set_margin_bottom(8)
        self._previewImage = Gtk.Image()
        box.pack_start(self._previewImage, False, False, 0)
        self._previewLabel = Gtk.Label()
        self._previewLabel.set_line_wrap(True)
        self._previewLabel.set_max_width_chars(45)
        self._previewLabel.set_halign(Gtk.Align.START)
        box.pack_start(self._previewLabel, False, False, 0)
        self._previewPopover.add(box)

    def _onThumbnailRightClicked(self, button, event, imageid):
        if event.button != 3:
            return False
        if not hasattr(self, '_previewPopover'):
            self._setupPreviewPopover()
        fpath = self.image_tiles[imageid][2]
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(fpath)
            w, h = pixbuf.get_width(), pixbuf.get_height()
            if w >= h:
                new_w, new_h = self._PREVIEW_SIZE, int(self._PREVIEW_SIZE * h / w)
            else:
                new_h, new_w = self._PREVIEW_SIZE, int(self._PREVIEW_SIZE * w / h)
            self._previewImage.set_from_pixbuf(
                pixbuf.scale_simple(new_w, new_h, GdkPixbuf.InterpType.BILINEAR))
        except Exception:
            return True
        parts = [imageid]
        if self.langdata:
            desc = self.langdata.get(imageid, {}).get("title", "")
            if desc:
                parts.append(desc)
        if self.imagedata:
            refs = re.sub(":0", "", "; ".join(
                self.imagedata["images"].get(imageid, {}).get('refs', [])))
            if refs:
                parts.append(refs)
        self._previewLabel.set_text("\n".join(parts))
        self._previewPopover.set_relative_to(button)
        self._previewPopover.show_all()
        return True  # consume event; prevent any default right-click handling

    def on_thumbnail_toggled(self, button, imageid):
        bibrefs = self.get_refs(imageid, default=[None])
        bibref = bibrefs[0] if len(bibrefs) else None
        title = self.langdata.get(imageid, {}).get("title", "") if self.langdata else ""
        val = (imageid, bibref, title)

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
            kwds = ", ".join(self.langdata.get(imageid, {}).get("kwds", []))
        else:
            desc = ""
            kwds = ""
        self.view.set("l_imgDesc", desc)
        self.view.set('l_imgKeywords', kwds)
        self._setLabelRowVisible("lb_imgDesc", "l_imgDesc", bool(desc))
        self._setLabelRowVisible("lb_imgKeywords", "l_imgKeywords", bool(kwds))

        if self.imagedata:
            refs = "; ".join(self.imagedata["images"].get(imageid, {}).get('refs', []))
            refs = re.sub(":0", "", refs)
        else:
            refs = ""
        self.view.set('l_imgRefs', refs)
        self._setLabelRowVisible("lb_imgRefs", "l_imgRefs", bool(refs))
