@echo on
REM Use this Batch file to build PTXprint Installer for Windows
REM Mark Penny and Martin Hosken, Last updated: 18-Mar-2024

REM Get rid of the build and dist folders before starting the new build process
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q Output

REM Call PyInstaller to create the "dist" folder
REM pyinstaller --log-level DEBUG --clean ptxprint.spec
pyinstaller ptxprint.spec
mkdir dist\ptxprint\share
xcopy /s /i /y /q C:\msys64\mingw64\share\locale dist\ptxprint\share\locale
xcopy /s /i /y /q C:\msys64\mingw64\share\fontconfig dist\ptxprint\share\fontconfig
xcopy /s /i /y /q C:\msys64\mingw64\share\glib-2.0 dist\ptxprint\share\glib-2.0
REM xcopy /s /i /y /q C:\msys64\mingw64\share\gtksourceview-1.0 dist\ptxprint\share\gtksourceview-4
REM xcopy /s /i /y /q C:\msys64\mingw64\share\icons dist\ptxprint\share\icons
xcopy /s /i /y /q C:\msys64\mingw64\share\themes dist\ptxprint\share\themes
xcopy /s /i /y /q python\lib\ptxprint\mo dist\ptxprint\mo
xcopy /s /i /y /q python\graphics\icons dist\ptxprint\share\icons
REM Then use a python script to build the #include list of only the needed icons from the Adwaita folders
python python\scripts\getstockicons -f inno -s dist\ptxprint -d "{app}" -i list-remove -i list-add -i pan-end -i pan-up -i pan-down -i object-select -i edit-clear -i edit-clear-rtl -i edit-clear-symbolic-rtl -i system-run -i view-grid -i software-update-available -i changes-prevent -i changes-allow -i folder-open -i help-about -i emblem-documents -i document-revert -i open-menu -i preferences-system-sharing -i view-dual -i go-bottom -i go-top -i format-justify-fill -i media-seek-forward -i media-seek-forward-symbolic-rtl.symbolic -i process-working-symbolic.svg python\lib\ptxprint\ptxprint.glade AdwaitaIcons.txt

REM Then call InnoSetup to build the final SetupPTXprint.exe file which is distributed
IF "%INNOSETUP_PATH%"=="" SET INNOSETUP_PATH="C:\Program Files (x86)\Inno Setup 6"
"%INNOSETUP_PATH%\ISCC.exe" InnoSetupPTXprint.iss

echo Windows Installer executable file is located in "Output" folder
