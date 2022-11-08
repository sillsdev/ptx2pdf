; Inno Setup Script
#define MyAppName "PTXprint"
#define MyAppVersion "2.2.39"
#define MyAppPublisher "SIL International"
#define MyAppURL "http://software.sil.org/"
#define MyAppExeName "PTXprint.exe"

[Setup]
AppId={{8C357785-AE61-4E0E-80BE-C537715D914B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
;PrivilegesRequiredOverridesAllowed=dialog
LicenseFile=docs\inno-docs\MIT License.txt
InfoBeforeFile=docs\inno-docs\ReleaseNotes.txt
InfoAfterFile=docs\inno-docs\AboutPTXprint.txt
;OutputBaseFilename=PTXprint-{#MyAppVersion}-Setup
OutputBaseFilename=SetupPTXprint({#MyAppVersion})
SetupIconFile=icon\62859-open-book-icon-setup.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english";    MessagesFile: "compiler:Default.isl"
Name: "french";     MessagesFile: "compiler:Languages\French.isl"
Name: "spanish";    MessagesFile: "compiler:Languages\Spanish.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "russian";    MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
;libcrypto-1_1-x64.dll,librsvg-2-2.dll,
[Files]
Source: "dist\ptxprint\PTXprint.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\ptxprint\ptxprint\gspawn-win64-helper.exe"; DestDir: "{app}"; Flags: ignoreversion
;Source: "python\scripts\diglotMerge.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\ptxprint\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "icons,locale,gspawn-win64-helper.exe"
Source: "dist\ptxprint\share\locale\ar\*"; DestDir: "{app}\share\locale\ar\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\en\*"; DestDir: "{app}\share\locale\en\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\es\*"; DestDir: "{app}\share\locale\es\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\fr\*"; DestDir: "{app}\share\locale\fr\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\hi\*"; DestDir: "{app}\share\locale\hi\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\hu\*"; DestDir: "{app}\share\locale\hu\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\id\*"; DestDir: "{app}\share\locale\id\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\ko\*"; DestDir: "{app}\share\locale\ko\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\my\*"; DestDir: "{app}\share\locale\my\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\pt\*"; DestDir: "{app}\share\locale\pt\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\ro\*"; DestDir: "{app}\share\locale\ro\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\ru\*"; DestDir: "{app}\share\locale\ru\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\th\*"; DestDir: "{app}\share\locale\th\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ptxprint\share\locale\zh_CN\*"; DestDir: "{app}\share\locale\zh_CN\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "xetex\*"; DestDir: "{app}\xetex\"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "cache"
#include "AdwaitaIcons.txt"
Source: "dist\ptxprint\share\icons\Adwaita\index.theme"; DestDir: "{app}\share\icons\Adwaita"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall 
;skipifsilent - removed this param so it can automatically (re)start the app after a silent install

[InstallDelete]
Type: files; Name: "{app}\ptxprint\Strong*.xml"
Type: files; Name: "{app}\ptxprint\cross_references.txt"