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
- img2pdf
- fonttools
- cairo

On Ubuntu (20.04 Focal Fossa) type the following to install the dependencies:
sudo apt install python3-gi gobject-introspection gir1.2-gtk-3.0 libgtk-3-0 gir1.2-gtksource-3.0 python3-cairo python3-regex python3-img2pdf texlive-xetex fonts-sil-charis 

To install the project in develop mode for Ubuntu 20.04 and python3.8:
sudo python3 setup.py develop 

When you launch PTXprint it will find your Paratext8 project folders by looking at 
~/.config/paratext/registry/LocalMachine/software/paratext/8/values.xml


## PTX2pdf



PTX2PDF is a XeTeX based macro package for typesetting USFM formatted (Paratext output) scripture files. This repo aims to be the common source, bringing together copies from other repositories. It also contains various examples of [usage and documentation](docs/home/README.md).

## Branches

There are various long term branches in this repository:

 * master. Current main development branch undergoing main release cycle. Should always be improving.
 * paratext. TeX macros used in Paratext

## User Support

The [user support area](docs/home/README.md) provides the following information:

 * an installation guide
 * a quick start user guide with sample project
 * a manual describing the files and parameters
 * a cookbook section answering frequently asked questions with real life examples

[This page](http://www.tug.org/xetex/) has an additional list of links related specifically to XeTeX.
