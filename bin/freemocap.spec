# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import sys
import os

from freemocap import __version__ as package_version

def get_mediapipe_path():
    import mediapipe
    mediapipe_path = mediapipe.__path__[0]
    return mediapipe_path

a = Analysis(
    ['../freemocap/__main__.py'],
    pathex=['../freemocap'],
    binaries=[],
    datas=[('../freemocap/gui/qt/style_sheet/qt_style_sheet.css','freemocap/gui/qt/style_sheet'),
                    ('../freemocap/assets/logo/freemocap-logo-black-border.svg', 'freemocap/assets/logo'),
                    ('../freemocap/data_layer/export_data/blender_stuff/blender_bpy_export_scripts/', 'freemocap/data_layer/export_data/blender_stuff/blender_bpy_export_scripts/'),
                    ('../freemocap/data_layer/generate_jupyter_notebook/', 'freemocap/data_layer/generate_jupyter_notebook/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pyqtgraph.canvas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

mediapipe_tree = Tree(get_mediapipe_path(), prefix='mediapipe', excludes=["*.pyc"])
a.datas += mediapipe_tree
a.binaries = filter(lambda x: 'mediapipe' not in x[0], a.binaries)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='freemocap',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='freemocap.app',
    icon='../freemocap/assets/logo/freemocap_skelly_logo.ico',
    bundle_identifier=None,
    info_plist={
      'CFBundleName': 'FreeMoCap',
      'CFBundleDisplayName': 'FreeMoCap',
      'CFBundleVersion': package_version,
      'CFBundleShortVersionString': package_version,
      'NSPrincipalClass': 'NSApplication',
      'NSAppleScriptEnabled': False,
      'NSCameraUsageDescription': 'Webcam can be opened by user to capture recordings for motion capture',
      'LSEnvironment': {
            'PATH': '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin',
        }
    },
)