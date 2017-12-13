# -*- mode: python -*-

block_cipher = None


a = Analysis(['sfq.py'],
             pathex=['.'],
             binaries=[],
             datas=[('COPYING.GPL', '.'), ('COPYING.Xiph', '.'), ('LICENSE', '.'), ('README.txt', '.'), ('flac.exe', '.'), ('ofr.exe', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='sfq',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='sfq')
