# PTXprint

## Introduction

PTXprint is a GTK-based GUI frontend to the Paratext print macros. It aims to make
using the best of the macros as easy as possible.

## Installation

PTXprint is very tied into Paratext and its project structure. Users should have
Paratext installed. PTXprint will access the Paratext project files directly but doesn't require Paratext to run while doing so.

PTXprint also has the following python dependencies:

- PyGObject. In particular GTK, Pango, GLib.
- regex. This is a package beyond re
- PIL (pillow)
- fonttools
- cairo
- numpy
- platformdirs
- usfmtc

### Ubuntu package installation

A recipe in LaunchPad provides a package built from the last tagged release:

`sudo add-apt-repository ppa:silnrsi/ptxprint`

`sudo apt update`

`sudo apt install python3-ptxprint`
(this will pull in the python3-usfmtc dependency)

You can also install both the python3-ptxprint and python3-usfmtc packages together manually:
After downloading them, go to the folder where they are located and type:

`sudo dpkg -i python3-ptxprint*.deb python3-usfmtc*.deb`

then launch it by typing:

`ptxprint`

There is also a desktop menu entry, just search in your menu for "ptxprint".
(you will get less error messages when starting it from the menu).

### Source installation

in the checked-out repository (if you haven't done so yet):

`git clone --depth=1 https://github.com/sillsdev/ptx2pdf.git`

```
sudo apt install build-essential cmake libgirepository-2.0-dev libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 texlive-xetex python3-setuptools gir1.2-poppler-0.18 gir1.2-gtksource-3.0 python3-numpy python3-gi gobject-introspection gir1.2-gtk-3.0 libgtk-3-0 gir1.2-gtksource-3.0 python3-cairo python3-regex python3-pil python3-venv
cd ptx2pdf
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel build
pip install .[gui]
```

Configuration files (like the default path to the translation project files) are stored in `~/.config/ptxprint/`
