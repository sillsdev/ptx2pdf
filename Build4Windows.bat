@echo on
REM Use this Batch file to build PTXprint Installer for Windows
REM Mark Penny and Martin Hosken, Last updated: 28-Nov-2025

REM Get rid of the build and dist folders before starting the new build process
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q Output

REM Call PyInstaller to create the "dist" folder
REM pyinstaller --log-level DEBUG --clean ptxprint.spec
pyinstaller ptxprint.spec
