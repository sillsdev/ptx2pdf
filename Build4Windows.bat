@echo on
REM Use this Batch file to build PTXprint Installer for Windows
REM Mark Penny and Martin Hosken, Last updated: 28-Nov-2025

set PPATH=C:\msys64\mingw64\bin\

REM Get rid of the build and dist folders before starting the new build process
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q Output

%PPATH%pip install usfmtc regex fonttools platformdirs Pillow numpy markdown-it-py WMI
REM Call PyInstaller to create the "dist" folder
REM pyinstaller --log-level DEBUG --clean ptxprint.spec
%PPATH%pyinstaller --log-level DEBUG ptxprint.spec
