REM Use this Batch file to build PTXprint Installer for Windows
REM Mark Penny and Martin Hosken, Last updated: 10-March-2020

REM Call PyInstaller to create the "dist" folder
pyinstaller ptxprint.spec

REM Then use a python script to build the #include list of only the needed icons from the Adwaita folders
python python\scripts\getstockicons -f inno -s dist\ptxprint -d "{app}" -i list-remove-symbolic.symbolic -i list-add-symbolic.symbolic -i pan-down-symbolic.symbolic python\lib\ptxprint\ptxprint.glade AdwaitaIcons.txt

REM Then call InnoSetup to build the final SetupPTXprint.exe file which is distributed
"C:\Program Files (x86)\Inno Setup 6\Compil32.exe" /cc InnoSetupPTXprint.iss

REM And finally call the Setup file to install it
REM call "Output\SetupPTXprint(0.4.0-beta).exe"