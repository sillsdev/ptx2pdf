#!/usr/bin/env python3

import gi, sys, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import xml.etree.ElementTree as et

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    imgdir = os.path.join(sys._MEIPASS, 'ptxprint')
else:
    imgdir = os.path.join(os.path.abspath(os.path.dirname(__file__)))

def main():
    if len(sys.argv) > 1:
        gladefile = sys.argv[1]
    else:
        return

    tree = et.parse(gladefile)
    for node in tree.iter():
        if node.get('name') in ('pixbuf', 'icon', 'logo'):
            node.text = os.path.join(imgdir, node.text)
    xml_text = et.tostring(tree.getroot(), encoding='unicode', method='xml')
    builder = Gtk.Builder()
    builder.add_from_string(xml_text)
    window = builder.get_object("w_splash")
    window.set_position(Gtk.WindowPosition.CENTER)
    window.set_default_size(400, 250)
    window.connect('destroy', Gtk.main_quit)
    window.set_auto_startup_notification(False)
    window.show_all()
    window.set_auto_startup_notification(True)
    Gtk.main()

if __name__ == "__main__":
    main()
