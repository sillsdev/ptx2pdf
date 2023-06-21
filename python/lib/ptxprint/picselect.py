import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import zipfile, appdirs

from ptxprint.utils import extraDataDir

def unpackImageset(dirname, filename):
    uddir = extraDataDir("imagesets", dirname, create=True)
    if uddir is None:
        return False
    with zipfile.ZipFile(filename) as zf:
        zf.extractall(path=uddir)
    return True

def getImageSets():
    uddir = os.path.join(appdirs.user_data_dir("ptxprint", "SIL"), "imagesets")
    return sorted([f for f in os.listdir(uddir) if os.path.isdir(os.path.join(uddir, f))])

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


class ThumbnailHolder(Gtk.ToggleButton):
    __cache__ = None
    __dimen__ = Gdk.Rectangle(100, 100)

    def __init__(self):
        super().__init__()
        self.fpath = None
        self.needsload = False
        self.set_hexpand(True)
        self.set_vexpand(True)
        #self.connect("draw", self.on_draw)

    def set_fpath(self, fpath):
        if fpath != self.fpath:
            self.fpath = fpath
            self.needsload = True
            self.fill_me()

    def clear(self):
        self.fpath = None
        self.needsload = False

    def do_draw(self, cr):
        print(f"Drawing {self.fpath}")
        if self.needsload and self.fpath is not None:
            self.fill_me()
        super().draw(cr)

    def fill_me(self):
        fill_me(self, self.fpath, self.__dimen__.width)
        self.needsload = False

if 0:
    def do_get_preferred_width(self):
        print(f"preferred_width for {self.picid}")
        return self.__cache__.get_preferred_width()

    def do_get_preferred_height(self):
        print(f"preferred_height for {self.picid}")
        return self.__cache__.get_preferred_height()

    def do_get_preferred_width_for_height(self, height):
        print(f"preferred_width_for_height for {self.picid}")
        return self.get_preferred_width()

    def do_get_preferred_height_for_width(self, width):
        print(f"preferred_height_for_width for {self.picid}")
        return self.get_preferred_height()

    def do_size_allocate(self, alloc):
        print(f"Allocating {self.picid} to {alloc.x}, (alloc.y) x {alloc.width}, {alloc.height}")
        super().do_size_allocate(alloc)
        self.alloc = alloc
        if self.child is not None:
            self.child.do_size_allocate(alloc)

    def get_allocate(self):
        print(f"Getting allocate for {self.picid}")
        return self.alloc

    def do_realize(self):
        print(f"Realizing f{self.picid}")
        super().do_realize()


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
    __dimen__ = Gdk.Rectangle(0, 100, 0, 100)

    def __init__(self, gridbox, gridcols):
        self.grid = gridbox
        self.gridcols = gridcols
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

    def set_images(self, fbase, imageids):
        children = self.grid.get_children()
        nchildren = len(children)
        nimages = len(imageids)
        if nchildren > nimages:
            for c in children[(nimages - nchildren):]:
                self.grid.remove(c)
        elif nchildren < nimages:
            for i in range(nimages - nchildren):
                j = nchildren + i
                rowj = j // self.gridcols
                colj = j % self.gridcols
                w = Gtk.ToggleButton()
                #w = ThumbnailHolder()
                self.grid.attach(w, colj, rowj, 1, 1)
                w.show()
        for i, c in enumerate(self.grid.get_children()):
            fpathbase = os.path.join(fbase, imageids[i])
            for e in (".jpg", ".tif"):
                fpath = fpathbase + e
                if os.path.exists(fpath):
                    break
            else:
                continue
            # print(f"{imageids[i]}: {fpath} ({colj},{rowj}) {self.grid.child_get_property(c, 'left-attach')}, {self.grid.child_get_property(c, 'top_attach')}")
            #c.set_fpath(fpath)
            fill_me(c, fpath, 100)
        self.grid.queue_resize()
        
        
class ThumbnailDialog:
    def __init__(self, dlg, view, gridbox, gridcols):
        self.dlg = dlg
        self.view = view
        self.artists = set()
        self.refs = ""
        self.filters = set()
        self.imageset = None
        self.thumbnails = Thumbnails(gridbox, gridcols)

    def run(self):
        ltv = self.view.builder.get_object("ls_artists")
        for r in ltv:
            if r[0]:
                self.artists.add(r[1].lower())
            else:
                self.artists.discard(r[1].lower())
        self.fill()
        response = self.dlg.run()
        self.dlg.hide()
        if response == Gtk.ResponseType.OK:
            return self.thumbnails.selected_thumbnails
        else:
            return None

    def set_imageset(self, s):
        self.imageset = s

    def add_artist(self, artid):
        self.artists.add(artid.lower())
        self.fill()

    def remove_artist(self, artid):
        self.artists.discard(artid.lower())
        self.fill()

    def set_filter(self, s):
        self.filters = set(s.split())

    def fill(self):
        print(self.artists)
        imagesetdir = extraDataDir("imagesets", self.imageset)
        if imagesetdir is None:
            return
        imagesdir = os.path.join(imagesetdir, "images")
        self.thumbnails.set_imagespath(imagesdir)
        imageids = set()
        for imagefile in os.listdir(imagesdir):
            (imageid, imageext) = os.path.splitext(imagefile)
            if not imageext.lower() in (".jpg", ".tif"):
                continue
            if len(self.artists) and imageid[:2].lower() not in self.artists:
                continue
            imageids.add(imageid)
        print(imageids)
        self.thumbnails.set_images(imagesdir, sorted(imageids))

