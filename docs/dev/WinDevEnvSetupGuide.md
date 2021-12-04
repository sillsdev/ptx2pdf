# How to set up the development environment for PTXprint on Windows

1. Download and install InnoSetup from here: https://jrsoftware.org/download.php/is.exe
2. Download and install MSYS2 from here:     https://www.msys2.org/ 
Link to exe: https://github.com/msys2/msys2-installer/releases/download/2021-11-30/msys2-x86_64-20211130.exe

Then, in the MSYS2 termninal that appears after installation:

3. To update the package database and base packages:
```
pacman -Syu
```
Don't run any of the other steps, and DON'T run this (as suggested): pacman -S --needed base-devel mingw-w64-x86_64-toolchain
The key issue here is NOT to have an installation of python under MSYS2, but to only have python under MINGW64 (otherwise nothing works).

4. Install the necessary packages:
```
pacman -S mingw-w64-x86_64-python mingw-w64-x86_64-python-pip mingw-w64-x86_64-python-setuptools mingw-w64-x86_64-gtksourceview3 mingw-w64-x86_64-python-pillow mingw-w64-x86_64-python-fonttools mingw-w64-x86_64-python-regex mingw-w64-x86_64-python-cairo mingw-w64-x86_64-python-gobject mingw-w64-x86_64-gtk3 mingw-w64-x86_64-glib2 mingw-w64-x86_64-libffi mingw-w64-x86_64-gcc mingw-w64-x86_64-glade
```

5. Install a couple of other important pieces:
```
pip3 install appdirs
pip3 install pyinstaller
```

Done! You are ready to build the .exe

```
./Build4Windows.bat
```

## For Working on the code

Install Git BASH https://gitforwindows.org/ (default options except Choosing the default editor: Use the Nano editor by default)
Open Git Bash terminal
```
git clone https://github.com/sillsdev/ptx2pdf.git
pwd (this will tell you which path to cd to in the next step)
```
Close Git Bash terminal

Open MSYS2 MinGW 64-bit terminal
```
cd c:/users/<your username>/ptx2pdf  (which is the path that you got from the previous pwd command)
python setup.py develop

python python/scripts/ptxprint -p test/projects -f test/fonts
```
