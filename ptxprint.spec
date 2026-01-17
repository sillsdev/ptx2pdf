# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import sys, os, platform, logging, shutil, datetime, json
from glob import glob
from subprocess import call, run
import xml.etree.ElementTree as et

print("sys.executable: ", sys.executable)
print("sys.path: ", sys.path)
print("Platform:", sys.platform)
if sys.platform.startswith("win"):
    bindir = "win32_x86_64"
else:
    bindir = sys.platform + "_" + platform.machine()
print("bindir:", bindir)

import usfmtc           # so we can find its data files

version="3.0.8"
logger = logging.getLogger(__name__)

#if 'Analysis' not in dir():
#    def printme(*a, **kw):
#        print(a, kw)
#    for a in ('Analysis', 'PYZ', 'EXE', 'COLLECT'):
#        setattr(__builtins__, a, printme)

# hunt around for the latest version of a file (where the version is at the end of the filename)
def anyver(p, path=".", ext=".dll"):
    spath = os.path.join(path, p)
    s = spath + "*{}".format(ext)
    allfiles = glob(s)
    best = None
    for a in allfiles:
        ver = a[len(spath):-(len(ext))]
        try:
            intver = int(ver)
        except ValueError:
            continue
        if best is None or intver > best:
            best = intver
    if best:
        res = p + str(intver)
    else:
        res = None
    return res

def getfiles(basedir, outbase, extin=[], excldirs=[], stripdir=False, debug=False):
    res = []
    for dp, dn, fs in os.walk(basedir):
        rpath = os.path.relpath(dp, basedir)
        rpath = "" if rpath == "." else rpath+"/"
        if any(x in dp for x in excldirs):
            continue
        for f in fs:
            if len(extin) and os.path.splitext(f)[1] not in extin:
                continue
            res.append((f'{dp}/{f}', f'{outbase}/{rpath}' if stripdir else f'{outbase}/{dp}'))
    if debug:
        logger.info(res)
    return res

def stripbinaries(binaries, basedir):
    allfiles = [f for dp, dn, fs in os.walk(basedir) for f in fs]
    res = []
    for b in binaries:
        if b[0] in allfiles:
            continue
        res.append(b)
    return res

def findall(root, fname, exts):
    for dp, dn, fn in os.walk(root or "."):
        if fname in fn:
            yield (fname, dp)
        for e in exts:
            f = fname + e
            if f in fn:
                yield (f, dp)

def parseglade(fname):
    doc = et.parse(fname)
    res = set()
    for e in doc.findall('.//object'):
        isstock = False
        for c in e:
            if c.tag == "property":
                n = c.get("name")
                if n == "label":
                    l = c.text
                elif n in ["use_stock", "use-stock"]:
                    isstock = True if c.text == "True" else False
        if isstock and l in icon_mappings:
            res.add(icon_mappings.get(l, l))
    return res

def process_icons(icons, src, dest):
    for i in sorted(icons):
        foundit = False
        for (f, p) in findall(src, i, ["-symbolic.symbolic.png", ".symbolic.png", ".png", ".svg"]):
            foundit = True
            t = p[p.find(src) + len(src) + 1:].replace("/",r"\\")
            d = dest + "\\" + t if dest else t
            s = src.replace("/", "\\") + "\\" + t + "\\" + f

        if not foundit:
            print(f"Failed to find source for {i}")

# mac build functions
def create_dmg_staging(app_name):
    # Create DMG staging directory in dist/dmg
    dmg_staging = os.path.join(DISTPATH, "dmg")
    if os.path.exists(dmg_staging):
        shutil.rmtree(dmg_staging)
    os.makedirs(dmg_staging)
    # Copy the .app bundle to dist/dmg
    shutil.copytree(os.path.join(DISTPATH, f"{app_name}.app"), os.path.join(dmg_staging, f"{app_name}.app"), symlinks=True)
    # Create Applications symlink in dist/dmg
    applications_link = os.path.join(dmg_staging, "Applications")
    if not os.path.exists(applications_link):
        os.symlink("/Applications", applications_link)
    return dmg_staging

def code_sign(app_name, dmg_staging):
    # Sign all Mach-O binaries
    print("Codesigning all binaries")
    sign_script = os.path.abspath("mac-sign-all-binaries.sh")
    app_bundle_path = os.path.join(dmg_staging, f"{app_name}.app")
    if not os.path.exists(sign_script):
        raise Exception(f"Signing script not found: {sign_script}")
    run(["bash", sign_script, app_bundle_path], check=True)

def create_dmg(app_name, version):
    for old in glob('*.dmg', root_dir=DISTPATH): os.remove(os.path.join(DISTPATH, old))
    dmg_path = os.path.join(DISTPATH, f"{app_name}_{version}.dmg")
    print(f"Creating {app_name}.dmg")
    run([
        "hdiutil", "create", "-volname", f"{app_name}",
        "-srcfolder", dmg_staging, "-ov", "-format", "UDZO", dmg_path
    ], check=True)
    return dmg_path

def notarize(dmg_path):
    # Notarize the DMG using xcrun notarytool
    apple_id = os.environ.get("NOTARIZATION_USERNAME")
    password = os.environ.get("NOTARIZATION_PASSWORD")
    team_id = os.environ.get("NOTARIZATION_TEAM")
    if apple_id and password and team_id:
        try:
            # Run xcrun notarytool submit and capture output
            print(f"Notarizing {dmg_path}")
            result = run([
                "xcrun", "notarytool", "submit", dmg_path,
                "--apple-id", apple_id,
                "--password", password,
                "--team-id", team_id,
                "--output-format", "json"
            ], check=True, capture_output=True, text=True)
            output_json = json.loads(result.stdout)
            request_id = output_json.get("id")
            if not request_id:
                raise Exception("No request ID found in notarytool output.")
            print(f"Notarization RequestID: {request_id}")
            # Run the mac-check-notarized.sh script with dmg path and request_id
            script_path = os.path.abspath("mac-check-notarized.sh")
            if not os.path.exists(script_path):
                raise Exception("No check notarized script found")
            run(["bash", script_path, dmg_path, request_id], check=True)
            print("Notarization check script complete.")
        except Exception as e:
            print(f"Notarization failed: {e}")
    else:
        print("Notarization skipped: NOTARIZATION_TEAM, NOTARIZATION_USERNAME, or NOTARIZATION_PASSWORD not set in environment.")


icon_mappings = {
"gtk-dialog-authentication": "dialog-password",
"gtk-dialog-error": "dialog-error",
"gtk-dialog-info": "dialog-information",
"gtk-dialog-question": "dialog-question",
"gtk-dialog-warning": "dialog-warning",
"gtk-close": "window-close",
"gtk-add": "list-add",
"gtk-justify-center": "format-justify-center",
"gtk-justify-fill": "format-justify-fill",
"gtk-justify-left": "format-justify-left",
"gtk-justify-right": "format-justify-right",
"gtk-goto-bottom": "go-bottom",
"gtk-cdrom": "media-optical",
"gtk-copy": "edit-copy",
"gtk-cut": "edit-cut",
"gtk-go-down": "go-down",
"gtk-execute": "system-run",
"gtk-quit": "application-exit",
"gtk-goto-first": "go-first",
"gtk-fullscreen": "view-fullscreen",
"gtk-leave-fullscreen": "view-restore",
"gtk-harddisk": "drive-harddisk",
"gtk-help": "help-contents",
"gtk-home": "go-home",
"gtk-info": "dialog-information",
"gtk-jump-to": "go-jump",
"gtk-goto-last": "go-last",
"gtk-go-back": "go-previous",
"gtk-missing-image": "image-missing",
"gtk-network": "network-idle",
"gtk-new": "document-new",
"gtk-open": "document-open",
"gtk-print": "document-print",
"gtk-print-error": "printer-error",
"gtk-print-paused": "printer-paused",
"gtk-print-preview": "document-print-preview",
"gtk-print-report": "printer-info",
"gtk-print-warning": "printer-warning",
"gtk-properties": "document-properties",
"gtk-redo": "edit-redo",
"gtk-remove": "list-remove",
"gtk-refresh": "view-refresh",
"gtk-revert-to-saved": "document-revert",
"gtk-go-forward": "go-next",
"gtk-save": "document-save",
"gtk-floppy": "media-floppy",
"gtk-save-as": "document-save-as",
"gtk-find": "edit-find",
"gtk-find-and-replace": "edit-find-replace",
"gtk-sort-descending": "view-sort-descending",
"gtk-sort-ascending": "view-sort-ascending",
"gtk-spell-check": "tools-check-spelling",
"gtk-stop": "process-stop",
"gtk-bold": "format-text-bold",
"gtk-italic": "format-text-italic",
"gtk-strikethrough": "format-text-strikethrough",
"gtk-underline": "format-text-underline",
"gtk-indent": "format-indent-more",
"gtk-unindent": "format-indent-less",
"gtk-goto-top": "go-top",
"gtk-delete": "edit-delete",
"gtk-undo": "edit-undo",
"gtk-go-up": "go-up",
"gtk-file": "text-x-generic",
"gtk-directory": "folder",
"gtk-about": "help-about",
"gtk-media-forward": "media-seek-forward",
"gtk-media-next": "media-skip-forward",
"gtk-media-pause": "media-playback-pause",
"gtk-media-play": "media-playback-start",
"gtk-media-previous": "media-skip-backward",
"gtk-media-record": "media-record",
"gtk-media-rewind": "media-seek-backward",
"gtk-media-stop": "media-playback-stop",
"gtk-zoom-100": "zoom-original",
"gtk-zoom-in": "zoom-in",
"gtk-zoom-out": "zoom-out",
"gtk-zoom-fit": "zoom-fit-best",
"gtk-select-all": "edit-select-all",
"gtk-clear": "edit-clear",
}

icons = set("""applications-system-symbolic changes-allow changes-prevent document-print-symbolic document-revert document-save-as-symbolic edit-clear edit-clear-rtl edit-clear-symbolic-rtl emblem-documents view-list-bullet-symbolic folder-documents folder-download folder-music folder-new-symbolic folder-open folder-open-symbolic folder-pictures-symbolic folder-videos-symbolic format-justify-fill go-bottom go-first-symbolic go-previous-symbolic go-next-symbolic go-last-symbolic go-top help-about-symbolic list-add list-remove media-seek-backward-symbolic media-seek-forward-symbolic object-select open-menu pan-down pan-end pan-up preferences-system-sharing printer software-update-available system-run user-desktop user-home x-office-document-symbolic text-x-generic-symbolic view-refresh-symbolic view-dual view-grid view-fullscreen-symbolic media-seek-backward-symbolic-rtl.symbolic media-seek-forward-symbolic-rtl.symbolic process-working-symbolic.svg""".split())

icons.update([icon_mappings["gtk-"+i] for i in \
        ("cdrom", "harddisk", "network", "directory", "floppy", "file", "home", "find")])
icons.update(parseglade("python/lib/ptxprint/ptxprint.glade"))

# Run this every time until a sysadmin adds it to the agent
# call([r'echo "y" | C:\msys64\usr\bin\pacman.exe -S mingw-w64-x86_64-python-numpy'], shell=True)

# add all the library dependency dlls (not python ones, but the dlls they typically call)
# including GTK, etc.
if sys.platform in ("win32", "cygwin"):
    mingwb = r'C:\msys64\mingw64\bin'
    binaries = [(f'{mingwb}\\{x}', 'ptxprint') for x in ('gspawn-win64-helper.exe', 'broadwayd.exe')] \
              + [(f'{mingwb}\\{x}.dll', '.') for x in
                    (anyver('libpoppler-', mingwb), 'libpoppler-glib-8', anyver('libpoppler-cpp-', mingwb), 'libcurl-4',
                     'libnspr4', 'nss3', 'nssutil3', 'libplc4', 'smime3', 'libidn2-0', 'libnghttp2-14', 
                     'libpsl-5', 'libssh2-1', 'libplds4', anyver('libunistring-', mingwb)) if x is not None] 
#             + [(x,'.') for x in glob('C:\\msys64\\mingw64\\bin\\*.dll')]
elif sys.platform == "darwin":
    hbpath = os.getenv('HOMEBREW_PREFIX')
    print("Homebrew path:", hbpath)
    binaries = []
    for a in (('poppler', 'libpoppler-glib.8'),):
        for dp, dn, f in os.walk(os.path.join(hbpath, 'Cellar', a[0])):
            print(dp, dn, f)
            if a[1]+'.dylib' in f:
                binaries.append((os.path.join(dp, a[1]+".dylib"), '.'))
else:
    binaries = []

                # all the binary files from the source tree that are used by the application.
                # These end up where specified (each entry is a 2 tuple: (source, target dir)
binaries = (binaries 
      + [('python/lib/ptxprint/PDFassets/border-art/'+y, 'ptxprint/PDFassets/border-art') for y in 
        ('A5 section head border.pdf', 'A5 section head border 2 column.pdf', 'A5 section head border-RTL-taller.pdf',
         'A5 page border.pdf', 'A5 page border - no footer.pdf', 'Verse number star.pdf', 'decoration.pdf',
         'Verse number rounded box.pdf')]
      + [('python/lib/ptxprint/PDFassets/watermarks/'+z, 'ptxprint/PDFassets/watermarks') for z in 
        ('A4-Draft.pdf', 'A5-Draft.pdf', 'A5-EBAUCHE.pdf',
         '5.8x8.7-Draft.pdf', 'A4-CopyrightWatermark.pdf', 'A5-CopyrightWatermark.pdf')]
      + [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
        ('Google-Noto-Emoji-Objects-62859-open-book.ico', '62859-open-book-icon(128).png', 
         'picLocationPreviews.png', 'marginNotesPreviews.png', 'sakura.css',
         'FRTtemplateBasic.txt', 'FRTtemplateAdvanced.txt',
         'top1col.png', 'top2col.png', 'topblue.png', 'topgreen.png', 'topgrid.png', 
         'tophrule.png', 'toporange.png', 'toppurple.png', 'topred.png', 'topvrule.png',
         'bot1col.png', 'bot2col.png', 'botblue.png', 'botgrid.png', 
         'botpurple.png', 'botred.png', 'botvrule.png', 
         'nibot1col.png', 'nibot2col.png', 'nibotblue.png', 'nibotgrid.png', 
         'nibotpurple.png', 'nibotred.png', 'nibotvrule.png')]
      + [('python/lib/ptxprint/unicode/*.bz2', 'ptxprint/unicode')]
      + [('python/lib/ptxprint/images/*.jpg', 'ptxprint/images')]
      + [('python/lib/ptxprint/syntax/*.*', 'ptxprint/syntax')]
      + [('fonts/' + f, 'fonts/' + f) for f in ('empties.ttf', 'SourceCodePro-Regular.ttf')]
      + [('src/mappings/*.tec', 'ptxprint/ptx2pdf/mappings')]
      + [('docs/documentation/OrnamentsCatalogue.pdf', 'ptxprint/PDFassets/reference')]
      + [('docs/documentation/PTXprintTechRef.pdf',  'ptxprint/PDFassets/reference')]
      + getfiles('resources', 'ptxprint', extin=['.zip'])
      + getfiles(f"xetex/bin/{bindir}", "ptxprint")
      + getfiles("xetex", "ptxprint", extin=[".tfm", ".pfm", ".pfb"])
      + getfiles("python/graphics/icons", "share/icons", stripdir=True)
      )

# data files are considered text and end up where specified by the tuple.
datas = (   [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
        ('ptxprint.glade', 'template.tex', 'picCopyrights.json', 'codelets.json', 'sRGB.icc', 'default_cmyk.icc', 'default_gray.icc', 'eng.vrs')]
      + [(f'python/lib/ptxprint/{x}/*.*y', f'ptxprint/{x}') for x in ('unicode', 'pdf', 'pdfrw', 'pdfrw/objects')]
      + getfiles("xetex", "ptxprint", excldirs=["bin", "tfm", "pfb"])
      + getfiles('resources', 'ptxprint', extin=['.sfm'])
              + [(f'src{d}/*.*', f'ptxprint/ptx2pdf{d}') for d in ('/', '/contrib', '/contrib/ornaments')]
              + [(f'src/mappings/*.map', f'ptxprint/ptx2pdf/mappings')]
      + [('python/lib/ptxprint/unicode/*.txt', 'ptxprint/unicode')]
      + [('python/lib/ptxprint/xrefs/*.*', 'ptxprint/xrefs')]
      + [('docs/inno-docs/*.txt', 'ptxprint')]
      + [(os.path.dirname(usfmtc.__file__)+"/"+x, "usfmtc") for x in ("*.vrs", "*.rng")]
    )

print("binaries:", binaries)
print("datas:", datas)

#    "pdfinish":  {"py": "python/scripts/pdfinish", "datas": [('python/lib/ptxprint/pdfinish.glade', 'ptxprint')]}
jobs = {
    "runsplash": {"py": "python/lib/ptxprint/runsplash.py", "datas": [('python/lib/ptxprint/splash.glade', 'ptxprint')]}
}
tcolls = []
for k, v in jobs.items():
    s = v.pop('py')
    a = Analysis([s],
             pathex = ['python/lib'],
             binaries = binaries,
             hookspath = [os.path.abspath("pyinstallerhooks")],
             runtime_hooks = [],
             excludes = ['tkinter', 'scipy'],
             win_no_prefer_redirects = False,
             win_private_assemblies = False,
             noarchive = False,
             **v)
    pz = PYZ(a.pure, a.zipped_data)
    e = EXE(pz, a.scripts, [],
          exclude_binaries=True,
          name = k,
          debug = False,
          bootloader_ignore_signals = False,
          strip = False,
          upx = False,
          onefile = False,
          upx_exclude = ['tcl'],
          runtime_tmpdir = None,
          contents_directory = '.',
          windowed=True,
          console = False)
    a.binaries = stripbinaries(a.binaries, f'xetex/bin/{bindir}')
    tcolls.append([e, a.binaries, a.zipfiles, a.datas])

a1 = Analysis(['python/scripts/ptxprint'],
            pathex =   ['python/lib'],
            binaries = binaries,
            datas = datas,
                # The registry tends not to get included
            hiddenimports = (['_winreg', 'gi.repository.win32'] if sys.platform.startswith("win") else []) \
                + ['gi.repository.fontconfig', 'gi.repository.Poppler', 'numpy._core._exceptions'],
            runtime_hooks = [],
            hookspath = [os.path.abspath("pyinstallerhooks")],
                # These can drift in from the analysis and we don't want them
            excludes = ['tkinter', 'scipy'],
            win_no_prefer_redirects = False,
            win_private_assemblies = False,
            noarchive = False)

a1.binaries = stripbinaries(a1.binaries, f'xetex/bin/{bindir}')
print("Binaries:", a1.binaries)
pyz1 = PYZ(a1.pure, a1.zipped_data)
app_name = 'PTXprint'
exe1 = EXE(pyz1,
          a1.scripts,
          [],
          exclude_binaries=True,
          name=f"{app_name}-app" if sys.platform == "darwin" else app_name,
          debug = False,
          bootloader_ignore_signals = False,
          strip = False,
          upx = False,
          onefile = False,
          upx_exclude = ['tcl'],
          runtime_tmpdir = None,
          contents_directory = '.',
          windowed=True,
          console = False,
          icon="icon/Google-Noto-Emoji-Objects-62859-open-book.ico")

# one has to do an analysis and exe for every application (what a pain)
colls = [[exe1, a1.binaries, a1.zipfiles, a1.datas]] + tcolls
allcolls = sum(colls, [])

# Then bring all the bits together here for the final build
coll = COLLECT(*allcolls,
               strip=False,
               upx=True,
               upx_exclude=['tcl'],
               name=app_name)

if sys.platform in ("win32", "cygwin"):
    srcdir = "C:/msys64/mingw64/share"
    for a in ('locale', 'fontconfig', 'glib-2.0', 'gtksourceview-3.0', 'themes'):
        shutil.copytree(f"{srcdir}/{a}", f"dist/ptxprint/share/{a}", dirs_exist_ok=True)
    process_icons(icons, f"{srcdir}/icons", "dist/PTXprint/share/icons")
    shutil.copy(f"{srcdir}/icons/Adwaita/index.theme", "dist/PTXprint/share/icons/Adwaita/index.theme")
    innosetup_path = os.getenv("INNOSETUP_PATH", "C:/Program Files (x86)/Inno Setup 6")
    run([f"{innosetup_path}/ISCC.exe", "InnoSetupPTXprint.iss"])

elif sys.platform == "darwin":
    app = BUNDLE(coll,
                name=f"{app_name}.app",
                icon='icon/Google-Noto-Emoji-Objects-62859-open-book.ico',
                bundle_identifier=f"org.sil.{app_name}",
                info_plist={
                    'NSPrincipalClass':'NSApplication',
                    'NSAppleScriptEnabled':False,
                    'CFBundleExecutable':f"{app_name}-app"
                })

    skip_codesign = os.environ.get("SKIP_CODESIGN") == "1"
    if  skip_codesign:
        sys.exit(0)

    dmg_staging = create_dmg_staging(app_name)
    code_sign(app_name, dmg_staging)
    dmg_path = create_dmg(app_name, version)
    if not os.environ.get("SKIP_NOTARIZE") == "1":
        notarize(dmg_path)
    shutil.rmtree(dmg_staging)

    # Generate download_info file
    for old in glob('*.download_info', root_dir=DISTPATH):
        os.remove(os.path.join(DISTPATH, old))
    with open(f"{dmg_path}.download_info", "wt") as outf:
        outf.write(f'''
            {{
                "description": "PTXprint macOS dmg"
                "date": "{datetime.date.today().isoformat()}",
                "version": "{version!s}",
                "category": "installer",
                "architecture": "{platform.machine()}",
                "platform": "mac",
                "type": "dmg",
                "name": "PTXPrint",
                "size": "{os.stat(dmg_path).st_size!s}"
                "file": "{app_name}_{version!s}.dmg",
            }}
        ''')
    print(f"Created download_info file: {dmg_path}.download_info")
