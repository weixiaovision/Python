# -*- mode: python -*-

block_cipher = None


a = Analysis(['newui.py'],
             pathex=['/Users/abc/PycharmProjects/Python/pythonpro/activity_easy_select'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='newui',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='newui.app',
             icon=None,
             bundle_identifier=None)