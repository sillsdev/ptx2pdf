# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import sys, os
from glob import glob
print("sys.executable: ", sys.executable)
print("sys.path: ", sys.path)
print("Platform:", sys.platform)
from subprocess import call
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
else:
    binaries = []

a1 = Analysis(['python/scripts/ptxprint'],
             pathex =   ['python/lib'],
                # all the binary files from the source tree that are used by the application.
                # These end up where specified (each entry is a 2 tuple: (source, target dir)
             binaries = binaries
                      + [('python/lib/ptxprint/PDFassets/border-art/'+y, 'ptxprint/PDFassets/border-art') for y in 
                            ('A5 section head border.pdf', 'A5 section head border 2 column.pdf', 'A5 section head border-RTL-taller.pdf',
                             'A5 page border.pdf', 'A5 page border - no footer.pdf', 'Verse number star.pdf', 'decoration.pdf',
                             'Verse number rounded box.pdf')]
                      + [('python/lib/ptxprint/PDFassets/watermarks/'+z, 'ptxprint/PDFassets/watermarks') for z in 
                            ('A4-Draft.pdf', 'A5-Draft.pdf', 'A5-EBAUCHE.pdf',
                             '5.8x8.7-Draft.pdf', 'A4-CopyrightWatermark.pdf', 'A5-CopyrightWatermark.pdf')]
                      + [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
                            ('Google-Noto-Emoji-Objects-62859-open-book.ico', '62859-open-book-icon(128).png', 
                             'picLocationPreviews.png',
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
                      + [('docs/documentation/PTXprintTechRef.pdf',  'ptxprint/PDFassets/reference')],
##                    + [('xetex/texmf-var/web2c/xetex/*.fmt', 'ptxprint/xetex/texmf-var/web2c/xetex')],
#                     + [('python/lib/ptxprint/mo/' + y +'/LC_MESSAGES/ptxprint.mo', 'mo/' + y + '/LC_MESSAGES') for y in os.listdir('python/lib/ptxprint/mo')]

                # data files are considered text and end up where specified by the tuple.
             datas =    [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
                            ('ptxprint.glade', 'template.tex', 'picCopyrights.json', 'codelets.json', 'sRGB.icc', 'default_cmyk.icc', 'default_gray.icc', 'eng.vrs')]
                      + [(f'python/lib/ptxprint/{x}/*.*y', f'ptxprint/{x}') for x in ('unicode', 'pdf', 'pdfrw', 'pdfrw/objects')]
#                      + sum(([('{}/*.*'.format(dp), 'ptxprint/{}'.format(dp))] for dp, dn, fn in os.walk('xetex') if dp not in ('xetex/bin/windows', ) and any(os.path.isfile(os.path.join(dp, f)) and '.' in f for f in fn)), [])
##					  + [(f"{dp}/*.*", f"ptxprint/{dp}") for dp, _, fn in os.walk("xetex") if dp != "xetex/bin/windows" and any("." in f for f in fn)]
					  + [(f'src{d}/*.*', f'ptxprint/ptx2pdf{d}') for d in ('/', '/contrib', '/contrib/ornaments')]
##					  + [(f'xetex/{d}/*', f'ptxprint/xetex/{d}') for d in ('texmf-dist', 'texmf-var')]
					  + [(f'src/mappings/*.map', f'ptxprint/ptx2pdf/mappings')]
                      + [('python/lib/ptxprint/unicode/*.txt', 'ptxprint/unicode')]
                      + [('python/lib/ptxprint/xrefs/*.*', 'ptxprint/xrefs')]
##                      + [('xetex/bin/windows/*.*', 'ptxprint/xetex/bin/windows')]
                      + [('docs/inno-docs/*.txt', 'ptxprint')]
#                      + [('src/*.tex', 'ptx2pdf'), ('src/ptx2pdf.sty', 'ptx2pdf'),
#                         ('src/usfm_sb.sty', 'ptx2pdf'), ('src/standardborders.sty', 'ptx2pdf')],
                      + [(os.path.dirname(usfmtc.__file__)+"/"+x, "usfmtc") for x in ("*.vrs", "*.rng")],
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
exe1 = EXE(pyz1,
          a1.scripts,
          [],
          exclude_binaries=True,
          name='PTXprint',
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
               name='ptxprint')
