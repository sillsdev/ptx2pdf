import gi
import os
import re
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import zipfile, json
import logging

logger = logging.getLogger(__name__)

from ptxprint.utils import _, extraDataDir, appdirs, allbooks, chaps, pycodedir
from usfmtc.reference import RefList, Ref, RefRange
from functools import reduce

image_extensions = {'.jpg', '.jpeg', '.tif', '.tiff', '.png', '.gif', '.bmp'}

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
            c = startbooks[self.book] + (self.chapter or 0)
            v = min(self.verse or 0, 127)
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
            firstc = self.chapter - 1
            lastc = self.chapter
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
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def getImageSets():
    uddir = os.path.join(appdirs.user_data_dir("ptxprint", "SIL"), "imagesets")
    if not os.path.exists(uddir):
        return None
    catalog_path = os.path.join(pycodedir(), "imagesets.json")
    logger.debug(f"{catalog_path=}")
    try:
        with open(catalog_path, encoding='utf-8') as f:
            catalog = {e['id']: e.get('name', e['id']) for e in json.load(f).get('imagesets', [])}
    except Exception:
        catalog = {}
    result = []
    for d in sorted(f for f in os.listdir(uddir) if os.path.isdir(os.path.join(uddir, f))):
        if d in catalog:
            name = catalog[d]
        else:
            illpath = os.path.join(uddir, d, "illustrations.json")
            try:
                with open(illpath, encoding='utf-8') as inf:
                    name = json.load(inf).get('name', d)
            except Exception:
                name = d
        result.append((d, name))
    return result or None

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
    def __init__(self, dlg, view, gridbox):
        self.dlg = dlg
        self.view = view
        self.artists = set()
        self.reflist = []
        self.filters = set()
        self.imageset = None
        self.grid = gridbox
        self.imagedata = None
        self.langdata = None
        self.tilesize = 100
        self.selected_thumbnails = set()
        self.reftext = None
        self._idleLoadId = None
        self._usedImageIds = set()
        self._usedAnchors = {}
        self._setupAlreadyUsedCss()
        self.dlg.connect("key-press-event", self._onDialogKeyPress)

    def _setupAlreadyUsedCss(self):
        css = Gtk.CssProvider()
        css.load_from_data(b"""
            flowboxchild.already-used {
                background-color: peachpuff;
                padding: 3px;
                border-radius: 4px;
            }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _getUsedImages(self):
        used = set()
        anchors = {}
        picinfos = getattr(self.view, 'picinfos', None)
        if picinfos is None:
            return used, anchors
        for pic in picinfos.get_pics():
            src = pic.get('src', '') or ''
            anchor = pic.get('anchor', '') or ''
            imgid = os.path.splitext(os.path.basename(src))[0].lower()
            if imgid:
                used.add(imgid)
                if anchor:
                    anchors.setdefault(imgid, []).append(anchor)
        return used, anchors

    def _applyUsedStyles(self):
        for imgid, (w, fbc, isLoaded, fpath) in self.image_tiles.items():
            sc = fbc.get_style_context()
            if imgid.lower() in self._usedImageIds:
                sc.add_class("already-used")
            else:
                sc.remove_class("already-used")

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
        last_imgset = self.view.userconfig.get("imagesets", "last", fallback=None)
        imgset = last_imgset or self.view.get('ecb_artPictureSet')
        if last_imgset:
            self.view.set('ecb_artPictureSet', last_imgset)
        # Re-apply any filter the user left active in a previous opening
        existing_ref = self.view.get('t_artRefRange') or ''
        existing_search = self.view.get('t_artSearch') or ''
        if existing_ref:
            self.reftext = existing_ref
        if existing_search:
            self.filters = set(c.lower() for c in existing_search.split())
        if not imgset:
            imagesets = getImageSets()
            if imagesets is None or not len(imagesets):
                return None
            else:
                imgset = imagesets[0][0]
        else:
            self.view.getBooks()
            reflist = self.view.bookrefs
            logger.debug(f"Start with bookrefs: {reflist}")
            if not existing_ref:
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
        if self.imagedata and 'sets' in self.imagedata:
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
            if not imageext.lower() in image_extensions:
                continue
            w = Gtk.ToggleButton()
            w.connect("toggled", self.on_thumbnail_toggled, imageid, imageext)
            w.connect("enter-notify-event", self.on_thumbnail_entered, imageid)
            w.connect("button-press-event", self._onThumbnailRightClicked, imageid)
            fbc = Gtk.FlowBoxChild()
            fbc.add(w)
            self.image_tiles[imageid] = (w, fbc, False, os.path.join(imagesdir, imagefile))
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
        entry = self.langdata.get(imgid, {})
        if any(f in x.lower() for x in entry.get('kwds', []) for f in filters):
            return True
        title_words = re.findall(r'\w+', entry.get('title', '').lower())
        if any(f in w for w in title_words for f in filters):
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
                self.doError(_("References must only use 3 letter book codes, etc."), str(e))
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
            if not imageext.lower() in image_extensions:
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
                    if any(r in e for e in self.reflist):
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
        self._usedImageIds, self._usedAnchors = self._getUsedImages()
        imageids = self._build_imageids(imagesdir)
        self.set_images(imagesdir, sorted(imageids))
        self._applyUsedStyles()
        self.disable_refresh()

    def imgkey(self, imgid, mode="ref"):
        if mode == "pop":
            pop = self.imagedata['images'].get(imgid, {}).get('pop', 0)
        else:
            pop = 0
        r = self.imgrefs.get(imgid)
        res = (r.first if isinstance(r, RefRange) else r).astag() if r is not None else "zzzz"+imgid
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

        for imgid in initial:
            w, fbc, isLoaded, fpath = self.image_tiles[imgid]
            if not isLoaded:
                fill_me(w, fpath, self.tilesize)
                self.image_tiles[imgid] = (w, fbc, True, fpath)
            self.grid.add(fbc)
            fbc.show_all()

        self._loadQueue = list(deferred)
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

        imgid = self._loadQueue.pop(0)
        w, fbc, isLoaded, fpath = self.image_tiles[imgid]
        if not isLoaded:
            fill_me(w, fpath, self.tilesize)
            self.image_tiles[imgid] = (w, fbc, True, fpath)
        self.grid.add(fbc)
        fbc.show_all()
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
        fpath = self.image_tiles[imageid][3]
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

    def on_thumbnail_toggled(self, button, imageid, imageext):
        bibrefs = self.get_refs(imageid, default=[None])
        bibref = bibrefs[0] if len(bibrefs) else None
        if self.reflist and bibrefs:
            for r in bibrefs:
                if r is not None and any(r in e for e in self.reflist):
                    bibref = r
                    break
        title = self.langdata.get(imageid, {}).get("title", "") if self.langdata else ""
        val = (imageid, bibref, title, imageext)

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
            raw_refs = self.imagedata["images"].get(imageid, {}).get('refs', [])
            parsed_refs = self.get_refs(imageid)
            placement_idx = 0
            if self.reflist:
                matching = self.imgrefs.get(imageid)
                if matching is not None:
                    for i, r in enumerate(parsed_refs):
                        if r is not None:
                            try:
                                if matching in r:
                                    placement_idx = i
                                    break
                            except Exception:
                                pass
            used_anchors = self._usedAnchors.get(imageid.lower(), [])
            ref_parts = []
            for i, (raw, parsed) in enumerate(zip(raw_refs, parsed_refs)):
                display = GLib.markup_escape_text(re.sub(":0", "", raw))
                is_placed = False
                for anchor_str in used_anchors:
                    try:
                        anchor_parsed = RefList(anchor_str, factory=TagableRef)[0]
                        if anchor_parsed in parsed:
                            is_placed = True
                            break
                    except (SyntaxError, IndexError, Exception):
                        pass
                if is_placed:
                    display = f'<span color="red">{display}</span>'
                if i == placement_idx:
                    display = f"<b>{display}</b>"
                ref_parts.append(display)
            refs = "; ".join(ref_parts)
        else:
            refs = ""
        self.view.set('l_imgRefs', refs, useMarkup=True)
        self._setLabelRowVisible("lb_imgRefs", "l_imgRefs", bool(refs))


def setupCatalog(view):
    cat = ImageSet(view)

class ImageSet:

    _methods = """onImageSetClicked onImagesetSelectAllToggled onImagesetQueryTooltip
                  onInstallFromZipActivated
               """.split()

    def __init__(self, view):
        self.view = view
        self.builder = view.builder
        view.register(self, self._methods)

    def doError(self, *a, **kw):
        self.view.doError(*a, **kw)

    def doStatus(self, *a, **kw):
        self.view.doStatus(*a, **kw)

    def onImageSetClicked(self, btn):
        if not hasattr(self, '_imagesetTvSetupDone'):
            self._setupImagesetTreeview()
            self._imagesetTvSetupDone = True
        self._populateImagesetList()
        # Reset Select All/None toggle without firing the handler
        sel_all = self.builder.get_object("c_imgSet_selectAll")
        sel_all.handler_block_by_func(self.onImagesetSelectAllToggled)
        sel_all.set_active(False)
        sel_all.handler_unblock_by_func(self.onImagesetSelectAllToggled)

        dialog = self.builder.get_object("dlg_getImageSet")
        response = dialog.run()
        dialog.hide()
        if response != Gtk.ResponseType.OK:
            return

        store = self.builder.get_object("ls_imagesets")
        # COL: 0=selected, 1=id, 7=description, 8=url, 9=license_text, 10=requires_terms
        selected_rows = [(row[1], row[8], row[10]) for row in store if row[0] and row[12]]
        if not selected_rows:
            return

        any_installed = False
        for imgset_id, url, requires_terms in selected_rows:
            filename = url.split("/")[-1]
            self.doStatus(_("Downloading '{}' — please wait...".format(imgset_id)))
            while Gtk.events_pending():
                Gtk.main_iteration()
            try:
                urlfile = urllib.request.urlopen(url)
                tzdir = extraDataDir("imagesets", "../zips", create=True)
                zfile = os.path.join(tzdir, filename)
                with open(zfile, 'wb') as f:
                    f.write(urlfile.read())
            except urllib.error.URLError:
                self.doStatus(_("ERROR: Download of '{}' failed. Check internet connection.".format(imgset_id)))
                while Gtk.events_pending():
                    Gtk.main_iteration()
                continue

            imgsetname = unpackImageset(zfile, self.project.path)
            if imgsetname is None:
                self.doError("Failed Image Set", secondary=f"'{imgset_id}' failed to download and/or install.")
                continue
            if imgsetname == "":
                f = os.path.join(self.project.path, "local", "figures")
                self.doStatus(_("Unzipped images to {}".format(f)))
                continue

            if requires_terms:
                uddir = extraDataDir("imagesets", imgsetname, create=False)
                if not self.displayReadmeFile(imgsetname, uddir):
                    try:
                        if uddir and len(uddir):
                            rmtree(uddir)
                            self.doStatus(_("Image Set '{}' removed — terms not accepted.".format(imgsetname)))
                    except OSError:
                        self.doStatus(_("Cannot delete folder! Image Set: {}".format(imgsetname)))
                    continue

            self._registerInstalledImageset(imgsetname)
            any_installed = True
            self.doStatus(_("Installed Image Set: {}".format(imgsetname)))

        if any_installed:
            self.onGetPicturesClicked(None)
        self.onHideStatusMsgClicked(None)

    def _setupImagesetTreeview(self):
        tv = self.builder.get_object("tv_imagesets")
        store = self.builder.get_object("ls_imagesets")
        tv.set_model(store)

        # Column indices in ls_imagesets:
        # 0=selected, 1=id, 2=name, 3=artist, 4=style, 5=filesize,
        # 6=license, 7=description, 8=url, 9=license_text,
        # 10=requires_terms, 11=status_text, 12=is_selectable

        r_toggle = Gtk.CellRendererToggle()
        r_toggle.connect("toggled", self._onImagesetRowToggled)
        col_sel = Gtk.TreeViewColumn("", r_toggle)
        col_sel.add_attribute(r_toggle, "active", 0)
        col_sel.add_attribute(r_toggle, "activatable", 12)
        tv.append_column(col_sel)

        for title, col_idx, min_w, expand in [
            ("Status",      11, 70,  False),
            ("Name",         2, 130, False),
            ("Artist",       3, 90,  False),
            ("Style",        4, 60,  False),
            ("Size",         5, 60,  False),
            ("License",      6, 90,  False),
            ("Description",  7, 120, True),
        ]:
            r = Gtk.CellRendererText()
            if expand:
                r.set_property("ellipsize", Pango.EllipsizeMode.END)
            col = Gtk.TreeViewColumn(title, r, text=col_idx)
            col.set_min_width(min_w)
            col.set_expand(expand)
            col.set_resizable(True)
            col.set_clickable(True)
            col.set_sort_column_id(col_idx)
            tv.append_column(col)

    def _onImagesetRowToggled(self, renderer, path):
        store = self.builder.get_object("ls_imagesets")
        it = store.get_iter(path)
        if store.get_value(it, 12):  # is_selectable
            store.set_value(it, 0, not store.get_value(it, 0))

    def onImagesetSelectAllToggled(self, btn):
        store = self.builder.get_object("ls_imagesets")
        active = btn.get_active()
        for row in store:
            if row[12]:  # is_selectable
                row[0] = active

    def onImagesetQueryTooltip(self, tv, x, y, keyboard_mode, tooltip):
        if keyboard_mode:
            path, col = tv.get_cursor()
            if path is None:
                return False
        else:
            bx, by = tv.convert_widget_to_bin_window_coords(x, y)
            result = tv.get_path_at_pos(bx, by)
            if result is None:
                return False
            path, col, _cx, _cy = result

        store = tv.get_model()
        it = store.get_iter(path)
        cols = tv.get_columns()
        if col not in cols:
            return False
        col_idx = cols.index(col)

        # Visual column order: 0=toggle, 1=status, 2=name, 3=artist,
        #                      4=style, 5=size, 6=license, 7=description
        if col_idx == 6:    # License column → show full license_text (model col 9)
            text = store.get_value(it, 9)
        elif col_idx == 7:  # Description column → show full description (model col 7)
            text = store.get_value(it, 7)
        else:
            return False

        if not text:
            return False
        tooltip.set_text(text)
        tv.set_tooltip_cell(tooltip, path, col, None)
        return True

    def _populateImagesetList(self):
        store = self.builder.get_object("ls_imagesets")
        store.clear()
        catalog = self._loadImagesetsCatalog()
        installed = set(imgid for imgid, _ in (getImageSets() or []))
        for item in catalog:
            imgid = item.get("id", "")
            already_installed = imgid in installed
            store.append([
                False,                                              # 0  selected
                imgid,                                             # 1  id
                item.get("name", ""),                              # 2  name
                item.get("artist", ""),                            # 3  artist
                item.get("style", ""),                             # 4  style
                item.get("filesize", ""),                          # 5  filesize
                item.get("license", ""),                           # 6  license
                item.get("description", ""),                       # 7  description
                item.get("url", ""),                               # 8  url
                item.get("license_text", ""),                      # 9  license_text
                item.get("requires_terms_acceptance", False),      # 10 requires_terms
                "\u2713 Installed" if already_installed else "",   # 11 status_text
                not already_installed,                             # 12 is_selectable
            ])

    def _loadImagesetsCatalog(self):
        catalog_path = os.path.join(pycodedir(), "imagesets.json")
        try:
            with open(catalog_path, 'r', encoding='utf-8') as f:
                return json.load(f).get("imagesets", [])
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return []

    def _imagesetName(self, imgsetname):
        """Return the display name for an installed imageset ID."""
        for item in self._loadImagesetsCatalog():
            if item.get('id') == imgsetname:
                return item.get('name', imgsetname)
        uddir = extraDataDir("imagesets", imgsetname)
        if uddir:
            illpath = os.path.join(uddir, "illustrations.json")
            try:
                with open(illpath, encoding='utf-8') as f:
                    return json.load(f).get('name', imgsetname)
            except Exception:
                pass
        return imgsetname

    def _registerInstalledImageset(self, imgsetname):
        """Add imgsetname to the picture-set combo box if not already present."""
        lsp = self.builder.get_object("ecb_artPictureSet")
        if not lsp.set_active_id(imgsetname):
            name = self._imagesetName(imgsetname)
            model = lsp.get_model()
            for i, row in enumerate(model):
                if name.casefold() < row[0].casefold():
                    lsp.insert(i, imgsetname, name)
                    break
            else:
                lsp.append(imgsetname, name)
            lsp.set_active_id(imgsetname)

    def displayReadmeFile(self, imgsetname, uddir):
        readme_path = os.path.join(uddir, "readme.txt")
        try:
            with open(readme_path, 'r') as f:
                readme_content = f.read()
        except FileNotFoundError:
            # No readme.txt — treat as freely available; no terms to accept.
            return True

        dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO, Gtk.ButtonsType.YES_NO, "readme")
        dialog.set_default_size(400, 300)
        dialog.set_title("Do you agree to the terms and conditions of use?")
        dialog.set_property("text", f"\nImage Set: {imgsetname}\n\n" + readme_content)
        response = dialog.run()
        dialog.destroy()
        return response == Gtk.ResponseType.YES

    def onInstallFromZipActivated(self, btn):
        """Handler for the 'Install from ZIP file...' link button in dlg_getImageSet."""
        imgsetfile = self.view.fileChooser("Select an Image Set ZIP file",
                filters={"Image Sets": {"patterns": ["*.zip"], "mime": "text/plain", "default": True},
                         "All Files": {"pattern": "*"}},
                multiple=False, basedir=os.path.join(self.project.path, "Bundles"))
        if imgsetfile is None:
            return True  # suppress browser open

        zfile = imgsetfile[0]
        imgsetname = unpackImageset(zfile, self.project.path)
        if imgsetname is not None and imgsetname != "":
            uddir = extraDataDir("imagesets", imgsetname, create=False)
            if not self.displayReadmeFile(imgsetname, uddir):
                try:
                    if uddir and len(uddir):
                        rmtree(uddir)
                        self.doStatus(_("Image Set '{}' removed — terms not accepted.".format(imgsetname)))
                except OSError:
                    self.doStatus(_("Cannot delete folder! Image Set: {}".format(imgsetname)))
                return True
            self._registerInstalledImageset(imgsetname)
            self.doStatus(_("Installed Image Set: {}".format(imgsetname)))
            # Refresh the list so the newly installed set shows as "✓ Installed"
            self._populateImagesetList()
        elif imgsetname == "":
            f = os.path.join(self.project.path, "local", "figures")
            self.doStatus(_("Unzipped images to {}".format(f)))
        else:
            self.doError("Faulty Image Set",
                         secondary="Please check that you have selected a valid Image Set (ZIP) file.")
        return True  # suppress browser open


