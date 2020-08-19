# Setting up PTXprint for Windows

## Assumed prerequisites
[Paratext 9](https://paratext.org/download/) 

## Additional tools
[Git BASH](https://gitforwindows.org/) (on *Choosing the default editor*, *Use the Nano editor by default* advised for novices)

[MSYS2](https://www.msys2.org/)

## Installation steps
1. Open an **MSYS2 MSYS** terminal and run
`pacman -Syu --noconfirm`.
If the terminal closes, open a new one.
Run
`pacman -Su mingw64/mingw-w64-x86_64-python mingw64/mingw-w64-x86_64-python-setuptools mingw64/mingw-w64-x86_64-gcc mingw64/mingw-w64-x86_64-python-cairo mingw64/mingw-w64-x86_64-python-gobject mingw64/mingw-w64-x86_64-gtksourceview3 mingw64/mingw-w64-x86_64-python-pillow mingw64/mingw-w64-x86_64-python-fonttools mingw64/mingw-w64-x86_64-python-regex --noconfirm`.
Close the **MSYS2 MSYS** terminal.

2. Open a **Git Bash** terminal and run
`git clone --single-branch --branch 1_0 https://github.com/sillsdev/ptx2pdf.git`, 
`cd ptx2pdf`,
`pwd` (this tells you where the ptx2pdf directory is for steps 3, 5, and 6).
Close the **Git Bash** terminal.

3. Open an **MSYS2 MinGW 64-bit** terminal and run
`cd c:/users/<your username>/ptx2pdf` (`cd` with the path from step 2),
`python setup.py install`.

4. PTXprint is now installed!

## Extra steps

5. Run
`python python/scripts/ptxprint -p test/projects -f test/fonts` 
and try out a project, or use `python python/scripts/ptxprint --help` to learn more about using PTXprint.

6. This guide will install the current stable release of PTXprint. To update in future, open a **Git Bash** terminal, and run `git init ptx2pdf`, `cd ptx2pdf`, `git pull`.