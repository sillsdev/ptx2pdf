@echo off
REM Use this Batch file to build PTXprint Installer for Windows
REM Mark Penny and Martin Hosken, Last updated: 10-March-2020

REM Call PyInstaller to create the "dist" folder
pyinstaller ptxprint.spec
mkdir dist\ptxprint\share
xcopy /s /i ..\msys64\mingw64\share\locale dist\ptxprint\share\locale
xcopy /s /i ..\msys64\mingw64\share\fontconfig dist\ptxprint\share\fontconfig
xcopy /s /i ..\msys64\mingw64\share\glib-2.0 dist\ptxprint\share\glib-2.0
xcopy /s /i ..\msys64\mingw64\share\gtksourceview-1.0 dist\ptxprint\share\gtksourceview-1.0
xcopy /s /i ..\msys64\mingw64\share\icons dist\ptxprint\share\icons
xcopy /s /i ..\msys64\mingw64\share\themes dist\ptxprint\share\themes

REM Then use a python script to build the #include list of only the needed icons from the Adwaita folders
python python\scripts\getstockicons -f inno -s dist\ptxprint -d "{app}" -i list-remove-symbolic.symbolic -i list-add-symbolic.symbolic -i pan-down-symbolic.symbolic python\lib\ptxprint\ptxprint.glade AdwaitaIcons.txt

REM Then call InnoSetup to build the final SetupPTXprint.exe file which is distributed
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /Qp InnoSetupPTXprint.iss

REM And finally call the Setup file to install it
echo Windows Installer executable file is located in "Output" folder
