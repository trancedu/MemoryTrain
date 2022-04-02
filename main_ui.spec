# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

datas_ = [('金融帝国博弈.txt', '.'),
 ('人类简史.txt', '.'),
 ('从林肯到奥巴马时代.txt', '.'),
 ('债务危机.txt', '.'),
 ('早晨从中午开始.txt', '.'),
 ('周杰伦.txt', '.'),
 ('一只特立独行的猪.txt', '.'),
 ('思考快与慢.txt', '.'),
 ('原则.txt', '.'),
 ('阳谋高手.txt', '.'),
 ('我们为什么会分手.txt', '.'),
 ('README.txt', '.'),
 ('自定义.txt', '.'),
 ('log.csv', '.')]

a = Analysis(['main_ui.py'],
             pathex=["/Users/duxueyuan/ml/MemoryTrain"],
             binaries=[],
             datas=datas_,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='记忆助手微软',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          icon="mind.ico",
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='记忆助手微软')
app = BUNDLE(coll,
             name='记忆助手微软.app',
             icon="mind.ico",
             bundle_identifier=None)
