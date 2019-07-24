# -*- mode: python -*-

block_cipher = None


a = Analysis(['src/tempo.py'],
             pathex=['/Users/chris/dev/latest/tempo'],
             binaries=[],
             datas=[
               ('icons', 'icons'),
             ],
             hiddenimports=['latest.main'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='tempo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )