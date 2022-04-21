# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import sys, os
from glob import glob
print("sys.executable: ", sys.executable)
print("sys.path: ", sys.path)
print("Platform:", sys.platform)

#if 'Analysis' not in dir():
#    def printme(*a, **kw):
#        print(a, kw)
#    for a in ('Analysis', 'PYZ', 'EXE', 'COLLECT'):
#        setattr(__builtins__, a, printme)

def anyver(p, path=".", ext=".dll"):
    s = os.path.join(path, p) + "*{}".format(ext)
    allfiles = glob(s)
    best = None
    print(f"{p=}, {allfiles}")
    for a in allfiles:
        ver = a[len(p):-(len(ext))]
        try:
            intver = int(ver)
        except ValueError:
            intver = ver
        if best is None or intver < best:
            best = intver
    if best:
        res = p + str(intver)
    else:
        res = None
    return res

mingwb = r'C:\msys64\mingw64\bin'
if sys.platform in ("win32", "cygwin"):
    binaries = [('C:\\msys64\\mingw64\\lib\\girepository-1.0\\{}.typelib'.format(x),
                                            'gi_typelibs') for x in
                    ('Gtk-3.0', 'GIRepository-2.0', 'Pango-1.0', 'GdkPixbuf-2.0', 
                     'GObject-2.0', 'fontconfig-2.0', 'win32-1.0', 'GtkSource-3.0', 'Poppler-0.18')] \
              + [(f'{mingwb}\\gspawn-win64-helper.exe', 'ptxprint')] \
			  + [('{}\\{}.dll'.format(mingwb, x), '.') for x in
					(anyver('libpoppler-', mingwb), 'libpoppler-glib-8', 'libpoppler-cpp-0',
                     anyver('libcurl-', mingwb),
					 'libnspr4', 'nss3', 'nssutil3', 'libplc4', 'smime3', 'libidn2-0', 'libnghttp2-14', 
					 'libpsl-5', 'libssh2-1', 'libplds4', 'libunistring-2') if x is not None] 
# 			  + [(x,'.') for x in glob('C:\\msys64\\mingw64\\bin\\*.dll')]
else:
    binaries = []

a = Analysis(['python/scripts/ptxprint'],
             pathex =   ['python/lib'],
             binaries = binaries
                      + [('python/lib/ptxprint/PDFassets/border-art/'+y, 'ptxprint/PDFassets/border-art') for y in 
                            ('A5 section head border.pdf', 'A5 section head border 2 column.pdf', 'A5 section head border(RTL).pdf',
                             'A5 page border.pdf', 'A5 page border - no footer.pdf', 'Verse number star.pdf', 'decoration.pdf')]
                      + [('python/lib/ptxprint/PDFassets/watermarks/'+z, 'ptxprint/PDFassets/watermarks') for z in 
                            ('A4-Draft.pdf', 'A5-Draft.pdf', 'A5-EBAUCHE.pdf',
                             '5.8x8.7-Draft.pdf', 'A4-CopyrightWatermark.pdf', 'A5-CopyrightWatermark.pdf')]
                      + [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
                            ('Google-Noto-Emoji-Objects-62859-open-book.ico', '62859-open-book-icon(128).png', 
                             'picLocationPreviews.png', 'default_cmyk.icc', 'cross_references.txt',
                             'FRTtemplateBasic.txt', 'FRTtemplateAdvanced.txt',
                             'Top1FalseFalse.png', 'Top1FalseTrue.png', 'Top2FalseFalse.png',
                             'Top2FalseTrue.png', 'Top2TrueFalse.png', 'Top2TrueTrue.png',
                             'Bottom1False.png', 'Bottom2False.png', 'Bottom2True.png')]
                      + [('python/lib/ptxprint/sfm/*.bz2', 'ptxprint/sfm')]
                      + [('python/lib/ptxprint/images/*.jpg', 'ptxprint/images')]
                      + [('fonts/' + f, 'fonts/' + f) for f in ('empties.ttf', 'SourceCodePro-Regular.ttf')]
                      + [('src/mappings/*.tec', 'ptx2pdf/mappings')],
#                     + [('python/lib/ptxprint/mo/' + y +'/LC_MESSAGES/ptxprint.mo', 'mo/' + y + '/LC_MESSAGES') for y in os.listdir('python/lib/ptxprint/mo')],
             datas =    [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
                            ('ptxprint.glade', 'template.tex', 'picCopyrights.json', 'sRGB.icc', 'default_cmyk.icc', 'eng.vrs',
                             'strongs.xml', 'strongs_info.xml', 'tsk.xml')]
                      + sum(([('python/lib/ptxprint/{}/*.*y'.format(x), 'ptxprint/{}'.format(x))] for x in ('sfm', 'pdf', 'pdfrw', 'pdfrw/objects')), [])
                      + [('python/lib/ptxprint/sfm/*.txt', 'ptxprint/sfm')]
                      + [('docs/inno-docs/*.txt', 'ptxprint')]
                      + [('src/*.tex', 'ptx2pdf'), ('src/ptx2pdf.sty', 'ptx2pdf'), ('src/usfm_sb.sty', 'ptx2pdf')],
             hiddenimports = ['_winreg'],
             hookspath = [],
             runtime_hooks = [],
             excludes = ['tkinter', 'numpy', 'scipy'],
             win_no_prefer_redirects = False,
             win_private_assemblies = False,
             noarchive = False)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(pyz,
          a.scripts,
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
          windowed=True,
          console = True,
          icon="icon/Google-Noto-Emoji-Objects-62859-open-book.ico")
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=['tcl'],
               name='ptxprint')
