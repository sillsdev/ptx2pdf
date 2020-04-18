# -*- mode: python ; coding: utf-8 -*-
# Syspath already contains these:
#  'C:/msys64/mingw64/lib/python37.zip',
#  'C:/msys64/mingw64/lib/python3.7',
#  'C:/msys64/mingw64/lib/python3.7/lib-dynload',
#  'C:/msys64/mingw64/lib/python3.7/site-packages',
#  'C:/msys64/mingw64/lib/python3.7/site-packages/setuptools-33.1.1-py3.7.egg',
#  'C:/msys64/mingw64/lib/python3.7/site-packages/pyinstaller-4.0.dev0+g4065d2c2-py3.7.egg'

block_cipher = None

a = Analysis(['python/scripts/ptxprint'],
             pathex =   ['python/lib', 'C:\\ptx2pdf',
                            'C:\\msys64\\mingw64\\lib',
                            'C:\\msys64\\usr\\lib\\python3.7\\site-packages',
                            'C:\\msys64\\mingw64\\lib\\python3.7\\lib-dynload',
                            'C:\\msys64\\mingw64\\lib\\python3.7',
                            'C:\\pyinstaller'],
             binaries = [('C:\\msys64\\mingw64\\lib\\girepository-1.0\\'+x+'.typelib',
                                                    'girepository-1.0/'+x+'.typelib') for x in 
                            ('Gtk-3.0', 'GIRepository-2.0', 'Pango-1.0',
                             'GObject-2.0', 'fontconfig-2.0', 'win32-1.0', 'GtkSource-3.0')]
                      + [('C:\\msys64\\mingw64\\lib\\python3.7\\site-packages\\cairo\\_cairo-cpython-37m.dll',
                        'cairo/_cairo-cpython-37m.dll')],
             datas =    [('python/lib/ptxprint/'+x, 'ptxprint') for x in 
                            ('ptxprint.glade', 'template.tex', 'A4-Grid.pdf', 'A4-Draft.pdf', 
                             'A5-Grid.pdf', 'A5-Draft.pdf', 'ps_cmyk.icc',
                             'A5 section head border.pdf', 'A5 section head border(RTL).pdf',
                             'A5 page border.pdf', 'Verse number star.pdf', 'decoration.pdf')]
                      + [('src/*.tex', 'ptx2pdf'),
                         ('src/mappings/*.tec', 'ptx2pdf/mappings')]
                      + [('python/lib/ptxprint/Google-Noto-Emoji-Objects-62859-open-book.ico', '.')],
             hiddenimports = ['_winreg'],
             hookspath = [],
             runtime_hooks = [],
             excludes = [],
             win_no_prefer_redirects = False,
             win_private_assemblies = False,
             noarchive = False)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PTXprint-0.4.7',
          debug = False,
          bootloader_ignore_signals = False,
          strip = False,
          upx = False,
          onefile = False,
          upx_exclude = [],
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
               upx_exclude=[],
               name='ptxprint')
