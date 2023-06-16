import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class ThumbnailWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Thumbnail Viewer")
        self.set_border_width(10)
        self.set_default_size(600, 400)

        # Create a vertical box as the main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)

        # Create a split pane
        split_pane = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        main_box.pack_start(split_pane, True, True, 0)

        # Create a box for the filters on the left side of the split pane
        filters_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        split_pane.pack1(filters_box, resize=True, shrink=False)

        # Create a scrolled window for the thumbnails grid
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        split_pane.pack2(scrolled_window, resize=True, shrink=False)

        # Create a grid to hold the thumbnails
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        scrolled_window.add(self.grid)

        # List of selected thumbnail filenames
        self.selected_thumbnails = []

        # Specify the folder path
        # folder_path = "D:\Reference\Bible related\BiblePictures\\testSample"
        folder_path = r"D:\Reference\Bible related\BiblePictures\images_96dpi"
        print(folder_path)

        # Add thumbnails from the specified folder
        self.add_thumbnails_from_folder(folder_path, "GT")  # Load GT images initially

        # Create checkboxes for the filters
        filter_checkboxes = []
        artist_filters = self.get_artist_filters(folder_path)

        for artist in artist_filters:
            checkbox = Gtk.CheckButton(label=artist)
            checkbox.connect("toggled", self.on_filter_toggled, artist)
            filters_box.pack_start(checkbox, True, False, 0)
            filter_checkboxes.append(checkbox)

    def get_artist_filters(self, folder_path):
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder does not exist: {folder_path}")
            return []

        # Read all .jpg files from the folder
        jpg_files = [file for file in os.listdir(folder_path) if file.lower().endswith(".jpg")]
        artists = {f[:2].upper() for f in jpg_files}
        return sorted(artists)

    def add_thumbnails_from_folder(self, folder_path, artist_filter):
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder does not exist: {folder_path}")
            return

        # Read all .jpg files from the folder
        jpg_files = [file for file in os.listdir(folder_path) if file.lower().endswith(".jpg")]
        
        # Add thumbnails for each .jpg file
        for filename in jpg_files:
            file_path = os.path.join(folder_path, filename)
            thumbnail_artist = os.path.splitext(os.path.basename(filename))[0][:2].upper()

            if artist_filter == thumbnail_artist:
                self.add_thumbnail(file_path)

    def add_thumbnail(self, file_path):
        # Create a thumbnail button with an image
        thumbnail_button = Gtk.ToggleButton()
        thumbnail_button.set_tooltip_text(os.path.splitext(os.path.basename(file_path))[0])
        thumbnail_button.connect("toggled", self.on_thumbnail_toggled, file_path)
        thumbnail_button.set_hexpand(True)
        thumbnail_button.set_vexpand(True)

        thumbnail_image = Gtk.Image()
        thumbnail_image.set_hexpand(True)
        thumbnail_image.set_vexpand(True)

        # Load the original image
        original_pixbuf = GdkPixbuf.Pixbuf.new_from_file(file_path)

        # Calculate the thumbnail size while preserving the aspect ratio
        max_size = 100  # Maximum size for the thumbnail
        width = original_pixbuf.get_width()
        height = original_pixbuf.get_height()
        aspect_ratio = width / height

        if width > height:
            thumbnail_width = max_size
            thumbnail_height = int(thumbnail_width / aspect_ratio)
        else:
            thumbnail_height = max_size
            thumbnail_width = int(thumbnail_height * aspect_ratio)

        # Scale the original image to the calculated thumbnail size
        thumbnail_pixbuf = original_pixbuf.scale_simple(thumbnail_width, thumbnail_height, GdkPixbuf.InterpType.BILINEAR)
        thumbnail_image.set_from_pixbuf(thumbnail_pixbuf)

        thumbnail_button.set_image(thumbnail_image)

        # Add the thumbnail button to the grid
        num_children = len(self.grid.get_children())
        row = num_children // 4
        column = num_children % 4
        self.grid.attach(thumbnail_button, column, row, 1, 1)

    def on_thumbnail_toggled(self, button, file_path):
        if button.get_active():
            self.selected_thumbnails.append(file_path)
        else:
            self.selected_thumbnails.remove(file_path)

        print("Selected thumbnails:", self.selected_thumbnails)

    def on_filter_toggled(self, checkbox, artist):
        folder_path = r"D:\Reference\Bible related\BiblePictures\images_96dpi"
        if checkbox.get_active():
            self.add_thumbnails_from_folder(folder_path, artist)
        else:
            for child in self.grid.get_children():
                thumbnail_button = child
                thumbnail_artist = os.path.splitext(os.path.basename(thumbnail_button.get_tooltip_text()))[0][:2].upper()

                if thumbnail_artist == artist:
                    self.grid.remove(thumbnail_button)

            self.grid.show_all()


win = ThumbnailWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
