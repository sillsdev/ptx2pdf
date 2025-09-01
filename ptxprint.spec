# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import sys, os, platform
from glob import glob
from subprocess import call
print("sys.executable: ", sys.executable)
print("sys.path: ", sys.path)
print("Platform:", sys.platform)
bindir = sys.platform + "_" + platform.machine()
print("bindir:", bindir)

import usfmtc           # so we can find its data files

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
    print(f"{p=}, {allfiles}: {res=}")
    return res

# Run this every time until a sysadmin adds it to the agent
# call([r'echo "y" | C:\msys64\usr\bin\pacman.exe -S mingw-w64-x86_64-python-numpy'], shell=True)

# add all the library dependency dlls (not python ones, but the dlls they typically call)
# including GTK, etc.
mingwb = r'C:\msys64\mingw64\bin'
if sys.platform in ("win32", "cygwin"):
    binaries = [(f'C:\\msys64\\mingw64\\lib\\girepository-1.0\\{x}.typelib',
                                            'gi_typelibs') for x in
                    ('Gtk-3.0', 'GIRepository-2.0', 'Pango-1.0', 'GdkPixbuf-2.0', 
                     'GObject-2.0', 'fontconfig-2.0', 'win32-1.0', 'GtkSource-3.0', 'Poppler-0.18')] \
              + [(f'{mingwb}\\gspawn-win64-helper.exe', 'ptxprint')] \
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
      + [('docs/documentation/PTXprintTechRef.pdf',  'ptxprint/PDFassets/reference')])
##                    + [('xetex/texmf_var/web2c/xetex/*.fmt', 'ptxprint/xetex/texmf_var/web2c/xetex')],
#                     + [('python/lib/ptxprint/mo/' + y +'/LC_MESSAGES/ptxprint.mo', 'mo/' + y + '/LC_MESSAGES') for y in os.listdir('python/lib/ptxprint/mo')]

                # data files are considered text and end up where specified by the tuple.
datas = (   [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
	    ('ptxprint.glade', 'template.tex', 'picCopyrights.json', 'codelets.json', 'sRGB.icc', 'default_cmyk.icc', 'default_gray.icc', 'eng.vrs')]
      + [(f'python/lib/ptxprint/{x}/*.*y', f'ptxprint/{x}') for x in ('unicode', 'pdf', 'pdfrw', 'pdfrw/objects')]
      + sum(([('{}/*.*'.format(dp), 'ptxprint/{}'.format(dp))] for dp, dn, fn in os.walk('xetex') if not dp.startswith('xetex/bin/') and any(os.path.isfile(os.path.join(dp, f)) and '.' in f for f in fn)), [])
      + sum(([('{}/*'.format(dp), 'ptxprint/{}'.format(dp))] for dp, dn, fn in os.walk('xetex/bin/'+bindir) if any(os.path.isfile(os.path.join(dp, f)) for f in fn)), [])
##					  + [(f"{dp}/*.*", f"ptxprint/{dp}") for dp, _, fn in os.walk("xetex") if dp != "xetex/bin/windows" and any("." in f for f in fn)]
			  + [(f'src{d}/*.*', f'ptxprint/ptx2pdf{d}') for d in ('/', '/contrib', '/contrib/ornaments')]
#					  + [(f'xetex/{d}/*', f'ptxprint/xetex/{d}') for d in ('texmf_dist', 'texmf_var', 'fonts')]
			  + [(f'src/mappings/*.map', f'ptxprint/ptx2pdf/mappings')]
      + [('python/lib/ptxprint/unicode/*.txt', 'ptxprint/unicode')]
      + [('python/lib/ptxprint/xrefs/*.*', 'ptxprint/xrefs')]
#                      + [('xetex/bin/'+bindir+'/*.*', 'ptxprint/xetex/bin/'+bindir)]
      + [('docs/inno-docs/*.txt', 'ptxprint')]
#                      + [('src/*.tex', 'ptx2pdf'), ('src/ptx2pdf.sty', 'ptx2pdf'),
#                         ('src/usfm_sb.sty', 'ptx2pdf'), ('src/standardborders.sty', 'ptx2pdf')],
      + [(os.path.dirname(usfmtc.__file__)+"/"+x, "usfmtc") for x in ("*.vrs", "*.rng")])

print("binaries:", binaries)
print("datas:", datas)

a1 = Analysis(['python/scripts/ptxprint'],
             pathex =   ['python/lib'],
	     binaries = binaries,
	     datas = datas,
                # The registry tends not to get included
             hiddenimports = ['_winreg'],
             hookspath = [],
             runtime_hooks = [],
                # These can drift in from the analysis and we don't want them
             excludes = ['tkinter', 'scipy'],
             win_no_prefer_redirects = False,
             win_private_assemblies = False,
             noarchive = False)
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
colls = [[exe1, a1.binaries, a1.zipfiles, a1.datas]]

#    "pdfinish":  {"py": "python/scripts/pdfinish", "datas": [('python/lib/ptxprint/pdfinish.glade', 'ptxprint')]}
jobs = {
    "runsplash": {"py": "python/lib/ptxprint/runsplash.py", "datas": [('python/lib/ptxprint/splash.glade', 'ptxprint')]}
}
for k, v in jobs.items():
    s = v.pop('py')
    a = Analysis([s],
             pathex = ['python/lib'],
             binaries = binaries,
             hookspath = [],
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
    colls.append([e, a.binaries, a.zipfiles, a.datas])
allcolls = sum(colls, [])

# Then bring all the bits together here for the final build
coll = COLLECT(*allcolls,
               strip=False,
               upx=True,
               upx_exclude=['tcl'],
               name=app_name)

if sys.platform == "darwin":
    import shutil
    import subprocess
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

    #
    # Create DMG staging directory in dist/dmg
    #
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

    #
    # Sign all Mach-O binaries
    #
    print("Codesigning all binaries")
    sign_script = os.path.abspath("mac-sign-all-binaries.sh")
    app_bundle_path = os.path.join(dmg_staging, f"{app_name}.app")
    if not os.path.exists(sign_script):
        raise Exception(f"Signing script not found: {sign_script}")
    subprocess.run(["bash", sign_script, app_bundle_path], check=True)

    #
    # Create the DMG from dist/dmg
    #
    dmg_path = os.path.join(DISTPATH, f"{app_name}.dmg")
    print(f"Creating {app_name}.dmg")
    subprocess.run([
        "hdiutil", "create", "-volname", f"{app_name}",
        "-srcfolder", dmg_staging, "-ov", "-format", "UDZO", dmg_path
    ], check=True)

    skip_notarize = os.environ.get("SKIP_NOTARIZE") == "1"
    if skip_notarize:
        sys.exit(0)

    #
    # Notarize the DMG using xcrun notarytool
    #
    apple_id = os.environ.get("NOTARIZATION_USERNAME")
    password = os.environ.get("NOTARIZATION_PASSWORD")
    team_id = os.environ.get("NOTARIZATION_TEAM")
    if apple_id and password and team_id:
        try:
            # Run xcrun notarytool submit and capture output
            print(f"Notarizing {dmg_path}")
            import json
            result = subprocess.run([
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
            subprocess.run(["bash", script_path, dmg_path, request_id], check=True)
            print("Notarization check script complete.")
        except Exception as e:
            print(f"Notarization failed: {e}")
    else:
        print("Notarization skipped: NOTARIZATION_TEAM, NOTARIZATION_USERNAME, or NOTARIZATION_PASSWORD not set in environment.")
    
    # Clean up the staging directory
    shutil.rmtree(dmg_staging)
