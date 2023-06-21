import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

from ptxprint.utils import extraDataDir

def unpackExtras(dirname, filename):
    uddir = extraDataDir("imagesets", dirname, create=True)
    if uddir is None:
        return
    with zipfile.ZipFile(filename) as zf:
        zf.extractall(path=uddir)

class ThumbnailHolder(Gtk.Widget):
    __gtype_name__ = "ThumbnailHolder"
    __cache__ = None

    def __init__(self):
        super().__init__()
        self.picid = ""
        self.child = None
        self.alloc = Gdk.Rectangle()

    def set_picid(self, picid):
        if picid != self.picid:
            self.child = None
            self.picid = picid

    def do_get_preferred_width(self):
        return self.__cache__.get_preferred_width()

    def do_get_preferred_height(self):
        return self.__cache__.get_preferred_height()

    def do_get_preferred_width_for_height(self, height):
        return self.get_preferred_width()

    def do_get_preferred_height_for_width(self, width):
        return self.get_preferred_height()

    def do_size_allocate(self, alloc):
        super().do_size_allocate(alloc)
        self.alloc = alloc
        if self.child is not None:
            self.child.do_size_allocate(alloc)

    def do_draw(self, cr):
        if self.child is None:
            self.child = self.__cache__.get_child(self, self.picid)
            if self.child is None:
                return
            self.child.do_size_allocate(self.alloc)
        self.child.do_draw(cr)

    def clear(self):
        self.child = None


class ThumbnailCache:

    def __init__(self, size, factoryfn, dimen):
        self.size = size
        self.factor = factoryfn
        self.dimen = dimen
        self.cache = {}
        self.entries = []
        self.curr_entry = 0
        ThumbnailHolder.__cache__ = self

    def get_child(self, parent, key):
        if key in self.cache:
            res = self.cache[key]
        else:
            res = self.add_child(key)
            if res is None:
                return None
        res.set_parent(parent)
        return res

    def add_child(self, key):
        res = factoryfn(key)
        if res is None:
            return None
        if len(self.entries) >= self.size:
            delkey = self.entries[self.curr_entry]
            oldchild = self.cache[delkey]
            if oldchild.get_parent() is not None:
                oldchild.get_parent().clear()
                oldchild.unparent()
            del self.cache[delkey]
            self.curr_entry += 1
            if self.curr_entry == self.size:
                self.curr_entry = 0
            self.entries[self.curr_entry] = key
            self.cache[key] = res
        else:
            self.cache[key] = res
            self.entries.append(key)
        return res

    def get_preferred_width(self):
        return dimen.width

    def get_preferred_height(self):
        return dimen.height
        

class Thumbnails:
    __dimen__ = Gdk.Rectangle(100, 100)

    def __init__(self, gridbox):
        self.grid = gridbox
        self.cache = ThumbnailCache(200, self.make_thumbnail, self.__dimen__)
        self.selected_thumbnails = set()
        ThumbnailHolder.__cache__ = self.cache

    def set_imagespath(self, imagespath):
        self.imagespath = imagespath

    def make_thumbnail(self, key):
        fpathbase = os.path.join(self.imagespath, key)
        for e in (".jpg", ".tif"):
            fpath = fpathbase + "." + e
            if os.path.exists(fpath):
                break
        else:
            return None

        thumbnail_button = Gtk.ToggleButton()
        thumbnail_button.set_tooltip_text(key)
        thumbnail_button.connect("toggled", self.on_thumbnail_toggled, key)
        thumbnail_button.set_hexpand(True)
        thumbnail_button.set_vexpand(True)

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
            thumbnail_width = self.__dimen__.width
            thumbnail_height = int(thumbnail_width / aspect_ratio)
        else:
            thumbnail_height = self.__diment__.height
            thumbnail_width = int(thumbnail_height * aspect_ratio)

        # Scale the original image to the calculated thumbnail size
        thumbnail_pixbuf = original_pixbuf.scale_simple(thumbnail_width, thumbnail_height, GdkPixbuf.InterpType.BILINEAR)
        thumbnail_image.set_from_pixbuf(thumbnail_pixbuf)

        thumbnail_button.set_image(thumbnail_image)
        return thumbnail_button

    def on_thumbnail_toggled(self, button, file_path):
        if button.get_active():
            self.selected_thumbnails.add(file_path)
        else:
            self.selected_thumbnails.discard(file_path)
        print("Selected thumbnails:", self.selected_thumbnails)

    def set_images(self, imageids):
        children = self.grid.get_children()
        nchildren = len(children)
        nimages = len(imageids)
        colwidth = self.grid.get_column_width(0) + self.grid.get_column_spacing()
        ncols = self.grid/get_allocated_width() // column_width
        if nchildren > nimages:
            for c in children[(nimages - nchildren):]:
                self.grid.remove(c)
        elif nchildren < nimages:
            for i in range(nimages - nchildren):
                j = nchildren + i
                rowj = j // ncols
                colj = j % ncols
                self.grid.attach(ThumbnailHolder(), colj, rowj, 1, 1)
        for i, c in self.grid.get_children():
            c.set_picid(imageids[i])
        
        
class ThumbnailDialog:
    def __init__(self, dlg, view, gridbox):
        self.dlg = dlg
        self.view = view
        self.artists = set()
        self.refs = ""
        self.filters = set()
        self.imageset = None
        self.thumbnails = Thumbnails(gridbox)

    def run(self):
        self.dlg.run()
        self.dlg.hide()

    def set_imageset(self, s):
        self.imageset = s

    def add_artist(self, artid):
        self.artists.add(artid)

    def remove_artist(self, artid):
        self.artists.discard(artid)

    def set_filter(self, s):
        self.filters = set(s.split())

    def fill(self):
        imagesetdir = extraDataDir("imagesets", self.imageset)
        if imagesetdir is None:
            return
        imagesdir = os.path.join(imagesetdir, "images")
        self.thumbnails.set_imagespath(imagesdir)
        imageids = set()
        for imagefile in os.listdir(imagesdir):
            (imageid, imageext) = os.splitext(imagefile)
            if not imageext.lower() in (".jpg", ".tif"):
                continue
            if len(self.artists) and imagid[:2].lower() not in self.artists:
                continue
            imageids.add(imageid)
        self.thumbnails.set_images(imageids)

