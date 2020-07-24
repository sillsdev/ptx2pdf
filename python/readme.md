# PTXprint

## Introduction

PTXprint is a GTK based gui frontend to the Paratext print macros. It aims to make
using the best of the macros as easy as possible.

## Installation

PTXprint is very tied into Paratext and its project structure. Users should have
Paratext installed. PTXprint will access the Paratext project files directly but doesn't require Paratext to run while doing so.

PTXprint also has the following python dependencies:

- PyGObject. In particular GTK, Pango, GLib.
- regex. This is a package beyond re
- PIL
- fonttools
- cairo


### Ubuntu package installation

The following works for both 18.04 (bionic) and 20.04 (focal), a recipe in LaunchPad provides daily builds from git master:

`sudo add-apt-repository ppa:silnrsi/ptxprint`

`sudo apt update`

`sudo apt install python3-ptxprint`

(86 packages to install with the various dependencies, 187 MB of archives, 628 MB of additional disk space).

then launch it by typing:

`ptxprint`  

There is also a desktop menu entry (but you get less error output).


### Source installation

On Ubuntu (20.04 Focal Fossa) type the following to install the dependencies:

`sudo apt install python3-gi gobject-introspection gir1.2-gtk-3.0 libgtk-3-0 gir1.2-gtksource-3.0 python3-cairo python3-regex python3-pil texlive-xetex fonts-sil-charis`

To install the project in develop mode for Ubuntu 20.04 and python3.8:

`sudo python3 setup.py develop`

When you launch PTXprint it will find your Paratext8 project folders by looking at
_~/.config/paratext/registry/LocalMachine/software/paratext/8/values.xml_
