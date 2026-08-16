#!/bin/bash
## -- mac-build-intel.sh
## status: works
##
## This script allows you to compile and run PTXprint (ptx2pdf) from SIL on macOS with Intel chip (not Apple Silicon).
## It needs to be executed on a macOS with Intel chip.
## This script can be used for automated building. (scp secure copy to target machine, run it, etc.)
##
## The end user (with only final binary PTXprint.app) needs still some work:
##   1. Install brew
##   2. install XeTeX with brew install xetex
##   3. Install font, https://fonts.google.com/specimen/Source+Code+Pro
##     Just double click on all font files within macOS Finder to install fonts
##
## target:
##   - for version ptxprint 2.9.5 - 3.0.32 some file patches are required.
##   - for version ptxprint 3.0.33 and after no file patch required anymore but this script.
##
## usage:
##   1. (only once) Install brew (Homebrew) on your macOS and the following packages:
##     % brew install gtk+3
##     % brew install  gtksourceview3
##     % brew install xetex
##     % npm install -g appdmg
##
##   2. (only once) for some reason a font is hard coded, so install it:
##     https://fonts.google.com/specimen/Source+Code+Pro
##     Just double click on all font files within macOS Finder to install fonts
##
##   Compile PTXprint (ptx2pdf)
##
##   3. Just download a ZIP Archive of PTXprint from https://github.com/sillsdev/ptx2pdf/tags
##      And unzip it.
##
##   4. Copy this script into main folder, for example ./ptx2pdf-3.0.37/mac-build-intel.sh
##
##   5. run it (compile). Open Terminal, cd to your main folder
##      % cd ./ptx2pdf-3.0.37/
##      % bash ./mac-build-intel.sh
##      This compiles the whole thing.
##
##   6. run it!
##      The product is in the ./dist/PTXprint.app
##      Double Click within macOS Finder as usual.
##      Check if it works, go to Font menu, try to select different font, if it works the font list must show.
##      Then create a PDF, if it works, a PDF preview must show up.
##
##   7. Troubleshooting
##      run within Terminal ./PTXprint.app/Contents/MacOS/PTXprint-app
##      See output.
##
## OS: macOS (with Intel chip, x86_64) - click on Apple Icon on top left,
##   then "About this Mac", Processor must say some thing including Intel.
##   If it sais Apple Silicon you have modern Apple chip. 
##
##
## History
## 2026-05may-28, seems to work for build .app but not app within .dmg.
## - The generated App WITHIN DMG is BAD and will not work. Does nothing. App does not show, but seems to use CPU forever.
##   (But the created .app outside the DMG will work)
##



## -- ad hoc code sign
export NOTARIZATION_CODESIGN_IDENTITY="-"
export SIGNING_IDENTITY_INSTALLER="-"
#export NOTARIZATION_TEAM=""
#export NOTARIZATION_USERNAME=""
#export NOTARIZATION_PASSWORD=""
# Notarization skipped: NOTARIZATION_TEAM, NOTARIZATION_USERNAME, or NOTARIZATION_PASSWORD not set in environment.





## -- get version as integer value
## pwd
## /Volumes/DATA/PTXprint/2.9.5-test/ptx2pdf-2.9.5
## basename `pwd`
## ptx2pdf-2.9.5
my_pwd=`pwd`
my_basename=`basename $my_pwd | cut -d- -f2`
ptxprint_version_str=`echo "$my_basename" | tr -d -c 0-9`
## "295"
## "3037"

echo "- ptxprint_version_str:$ptxprint_version_str"




## -- find out where you have your homebrew (brew) installed
export HOMEBREW_PREFIX=`brew config | grep HOMEBREW_PREFIX | cut -f2 -d: | awk '{$1=$1};1'`
## /usr/local
echo "-- your HOMEBREW_PREFIX is:"
echo "$HOMEBREW_PREFIX"




## -- patch source code
## -- NOTE: With version 3.0.33 no patches required?

## -- make sure you use Gtk 3 else your app will crash later
## main.py add on top:
## import gi
## gi.require_version('Gtk', '3.0')
#--dry-run
# -R reverse
# -b backup


## -- get version of ptxprint
## ./python/lib/ptxprint/version.py
## VersionStr = "3.0.37"
## GitVersionStr = "3.0.37"
## ConfigVersion = "3.01"


if [ $ptxprint_version_str -gt 3032 ]; then
  ## -- no source file patches needed
  ## -- NOTE: With version 3.0.33 no patches required?
  echo "- you compile version 3.0.33 or later"

else
  ## -- some source file patches needed
  ## [PYI-14051:ERROR] Failed to execute script 'ptxprint' due to unhandled exception: gtk-builder-error-quark: .:15738:56 Invalid object type 'GtkSourceBuffer' (6)
  ## gtkview.py add about on top:
  ## gi.require_version('GtkSource', '3.0')
  ## gi.require_version('Gtk', '3.0')

  echo "- you compile version 3.0.32 or earlier, some source code patches needed"

  patch -R -b ./python/lib/ptxprint/main.py --ignore-whitespace << 'EOF'
2,3d1
< import gi
< gi.require_version('Gtk', '3.0')
EOF



  patch -R -b ./python/lib/ptxprint/gtkview.py --ignore-whitespace << 'EOF'
9d8
< gi.require_version('GtkSource', '3.0')
EOF
  
fi






## -- the following lines are taken from https://github.com/sillsdev/ptx2pdf/mac-build.sh
python3 -m venv --system-site-packages _venv
source _venv/bin/activate
pip3 install -e .
pip3 install pyinstaller




## -- build

## -- the following command will compile the .app and .dmg
## -- if you need to re-compile things, just call this line and do the patch below again
pyinstaller ptxprint.spec -y



## -- patch fix the app binary within ./dist so that it can find xetex

echo "- fix the app so that if finds xetex"
mkdir -p ./dist/PTXprint.app/Contents/Frameworks/ptxprint/xetex/bin/darwin_x86_64/
ln -s /usr/local/bin/fc-list         ./dist/PTXprint.app/Contents/Frameworks/ptxprint/xetex/bin/darwin_x86_64
ln -s /Library/TeX/texbin/xetex      ./dist/PTXprint.app/Contents/Frameworks/ptxprint/xetex/bin/darwin_x86_64
ln -s /Library/TeX/texbin/xdvipdfmx  ./dist/PTXprint.app/Contents/Frameworks/ptxprint/xetex/bin/darwin_x86_64


## -- run app from command line
echo "- Run app with ./dist/PTXprint.app/Contents/MacOS/PTXprint-app"
echo "- Or just double click PTXprint-app.app within macOS Finder as usual."
echo "- You can copy PTXprint-app.app in /Applications folder."



## -- show codesign (adhoc)
## https://stories.miln.eu/graham/2024-06-25-ad-hoc-code-signing-a-mac-app/
## Ad hoc code signing is a type of digital signature created for a specific,
## temporary purpose without using a verifiable developer identity.
## In operating systems like macOS, it acts as a "seal" applied to a program
## so the system knows the code hasn't been tampered with, but it does not
## prove who wrote it.

#codesign -dv ./dist/PTXprint.app 
#Executable=
#Identifier=org.sil.PTXprint
#Format=app bundle with Mach-O thin (x86_64)
#CodeDirectory v=20400 size=68009 flags=0x2(adhoc) hashes=2119+3 location=embedded
#Signature=adhoc
#Info.plist entries=11
#TeamIdentifier=not set
#Sealed Resources version=2 rules=13 files=1635
#Internal requirements count=0 size=12


#echo "-- Create ZIP archive of .app"
cd ./dist
zip -9 -y -r -q PTXprint.zip PTXprint.app
#Flag descriptions:
#-9: compress better
#-y: store symbolic links as the link instead of the referenced file
#-r: recurse into directories
#-q: quiet operation

echo "-- Checksum ZIP archive with sha512sum"
sha256sum PTXprint.zip > sha256sum.txt

cd ..

echo "- Note: Do not forget to install XeTeX with brew install xetex if you don't have it already"

echo "- ALL DONE."



## -- create .pgk from .app
## status: does not work now
#productbuild --component dist/PTXprint.app /Applications dist/PTXprint.pkg     --sign "${SIGNING_IDENTITY_INSTALLER}"
## ./dist/PTXprint.pkg



## EOF.
