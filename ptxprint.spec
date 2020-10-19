# -*- mode: python ; coding: utf-8 -*-
# Syspath already contains these:
#  'C:/msys64/mingw64/lib/python37.zip',
#  'C:/msys64/mingw64/lib/python3.7',
#  'C:/msys64/mingw64/lib/python3.7/lib-dynload',
#  'C:/msys64/mingw64/lib/python3.7/site-packages',
#  'C:/msys64/mingw64/lib/python3.7/site-packages/setuptools-33.1.1-py3.7.egg',
#  'C:/msys64/mingw64/lib/python3.7/site-packages/pyinstaller-4.0.dev0+g4065d2c2-py3.7.egg'

block_cipher = None
import sys
if sys.platform == "win32":
     pathex =   ['C:\\ptx2pdf',
        'C:\\msys64\\mingw64\\lib',
        'C:\\msys64\\usr\\lib\\python3.7\\site-packages',
        'C:\\msys64\\mingw64\\lib\\python3.7\\lib-dynload',
        'C:\\msys64\\mingw64\\lib\\python3.7',
        'C:\\pyinstaller']
     binaries = [('C:\\msys64\\mingw64\\lib\\girepository-1.0\\'+x+'.typelib',  #'
                                            'girepository-1.0/'+x+'.typelib') for x in 
                    ('Gtk-3.0', 'GIRepository-2.0', 'Pango-1.0',
                     'GObject-2.0', 'fontconfig-2.0', 'win32-1.0', 'GtkSource-3.0')] \
              + [('C:\\msys64\\mingw64\\lib\\python3.7\\site-packages\\cairo\\_cairo-cpython-37m.dll',
                'cairo/_cairo-cpython-37m.dll')] \
              + [('C:\\msys64\\mingw64\\bin\\gspawn-win64-helper.exe', 'ptxprint')]
else:
    pathex = []
    binaries = []

a = Analysis(['python/scripts/ptxprint', 'python/scripts/usfmerge'],
             pathex =   ['python/lib'] + pathex,
             binaries = binaries
                      + [('python/lib/ptxprint/PDFassets/border-art/'+y, 'ptxprint/PDFassets/border-art') for y in 
                            ('A5 section head border.pdf', 'A5 section head border(RTL).pdf',
                             'A5 page border.pdf', 'Verse number star.pdf', 'decoration.pdf')]
                      + [('python/lib/ptxprint/PDFassets/watermarks/'+z, 'ptxprint/PDFassets/watermarks') for z in 
                            ('A4-Grid.pdf', 'A4-Draft.pdf', 'A5-Grid.pdf', 'A5-Draft.pdf',
                             '5.8x8.7-12mmBorderDraft.pdf', '5.8x8.7-Draft.pdf', 'BSI-12mmBorder.pdf',
                             'A4-12mmBorder.pdf', 'A5-10mmBorder.pdf', 'A4-CopyrightWatermark.pdf', 'A5-CopyrightWatermark.pdf')]
                      + [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
                            ('Google-Noto-Emoji-Objects-62859-open-book.ico', '62859-open-book-icon(128).png', 'ps_cmyk.icc')]
                      + [('src/mappings/*.tec', 'ptx2pdf/mappings')],
             datas =    [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
                            ('ptxprint.glade', 'template.tex')]
                      + [('python/lib/ptxprint/sfm/*.*y', 'ptxprint/sfm')]
                      + [('docs/inno-docs/*.txt', 'ptxprint')]
                      + [('src/*.tex', 'ptx2pdf'), ('src/ptx2pdf.sty', 'src/usfm_sb.sty', 'ptx2pdf')],
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
          console = False,
          icon="icon/Google-Noto-Emoji-Objects-62859-open-book.ico")
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=['tcl'],
               name='ptxprint')
