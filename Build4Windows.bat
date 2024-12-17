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
python python\scripts\getstockicons -f inno -s dist\ptxprint -d "{app}" -i changes-allow -i changes-prevent -i document-print -i document-revert -i document-save-as-symbolic -i edit-clear -i edit-clear-rtl -i edit-clear-symbolic-rtl -i emblem-documents -i folder-documents -i folder-download -i folder-music -i folder-new-symbolic -i folder-open -i folder-open-symbolic -i folder-pictures-symbolic -i folder-videos-symbolic -i format-justify-fill -i go-bottom -i go-top -i help-about -i list-add -i list-remove -i media-seek-forward -i object-select -i open-menu -i pan-down -i pan-end -i pan-up -i preferences-system-sharing -i printer -i software-update-available -i system-run -i user-desktop -i user-home -i view-dual -i view-grid -i media-seek-forward-symbolic-rtl.symbolic -i process-working-symbolic.svg python\lib\ptxprint\ptxprint.glade AdwaitaIcons.txt

REM Then call InnoSetup to build the final SetupPTXprint.exe file which is distributed
IF "%INNOSETUP_PATH%"=="" SET INNOSETUP_PATH="C:\Program Files (x86)\Inno Setup 6"
"%INNOSETUP_PATH%\ISCC.exe" InnoSetupPTXprint.iss

echo Windows Installer executable file is located in "Output" folder
