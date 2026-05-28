# How to compile and run PTXprint on macOS for macOS with Intel chips

Date: 2026-05may-28

## Ideas for future versions

- Maybe there should be a Settings > TeTeX path input box where user can setup which TeTeX will be used.

## Instructions

- Just follow the instructions in the script below.

## Issues
- The created .app within the DMG does not work (but the .app outside the dmg does work)

```
#!/bin/bash
## -- mac-build-intel.sh
## status: works
##
## History
## 2026-05may-28, seems to work for build .app but not app within .dmg.
## - The generated App WITHIN DMG is BAD and will not work. Does nothing. App does not show, but seems to use CPU forever.
##   (But the created .app outside the DMG will work)
##
## Instructions
## 1. install brew (Homebrew) on your macOS and the following packages:
##   % brew install gtk+3
##   % brew install  gtksourceview3
##   % brew install xetex
##   % npm install -g appdmg
##
## 2. for some reason a font is hard coded, so install it:
##   https://fonts.google.com/specimen/Source+Code+Pro
##   Just double click on all font files within macOS Finder to install fonts
##
## 3. follow the instructions here
##


echo "mac-build-intel.ch -- Build App for Intel based Macs."
echo "NOTE: This is NOT an automated script!"
echo "Instead you need to do copy past manually to your command line terminal and patch some code manually."
exit


## -- get source code from github

git clone --depth=1 https://github.com/sillsdev/ptx2pdf.git

cd ptx2pdf


## -- prepare for build
## add your Apple Code Sign identity here:
export NOTARIZATION_CODESIGN_IDENTITY="1234567890"


## -- find out where you have your homebrew (brew) installed
export HOMEBREW_PREFIX=`brew config | grep HOMEBREW_PREFIX | cut -f2 -d: | awk '{$1=$1};1'`
## /usr/local
echo "-- your HOMEBREW_PREFIX is:"
echo "$HOMEBREW_PREFIX"


## -- the following lines are taken from https://github.com/sillsdev/ptx2pdf/mac-build.sh
python3 -m venv --system-site-packages _venv
source _venv/bin/activate
pip3 install -e .
pip3 install pyinstaller




## -- patch source code

## -- make sure you use Gtk 3 else your app will crash later

## main.py add on top:
## import gi
## gi.require_version('Gtk', '3.0')


## [PYI-14051:ERROR] Failed to execute script 'ptxprint' due to unhandled exception: gtk-builder-error-quark: .:15738:56 Invalid object type 'GtkSourceBuffer' (6)
## gtkview.py add about on top:
## gi.require_version('GtkSource', '3.0')
## gi.require_version('Gtk', '3.0')




## -- build

## -- the following command will compile the .app and .dmg
## -- if you need to re-compile things, just call this line and do the patch below again
pyinstaller ptxprint.spec -y




## -- patch fix the app binary within ./dist so that it can find xetex

echo "fix the app so that if finds xetex"
mkdir -p ./dist/PTXprint.app/Contents/Frameworks/ptxprint/xetex/bin/darwin_x86_64/
ln -s /usr/local/bin/fc-list         ./dist/PTXprint.app/Contents/Frameworks/ptxprint/xetex/bin/darwin_x86_64
ln -s /Library/TeX/texbin/xetex      ./dist/PTXprint.app/Contents/Frameworks/ptxprint/xetex/bin/darwin_x86_64
ln -s /Library/TeX/texbin/xdvipdfmx  ./dist/PTXprint.app/Contents/Frameworks/ptxprint/xetex/bin/darwin_x86_64


## -- run app from command line
echo "Run app with ./dist/PTXprint.app/Contents/MacOS/PTXprint-app"
echo "Or just double click PTXprint-app.app within macOS Finder as usual."
echo "You can copy PTXprint-app.app in /Applications folder."




## EOF.
```
