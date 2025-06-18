# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[('gui_ensambler.py', '.'), ('gui_functionalities.py', '.'), ('functions.py', '.'), ('languages_categories.json', '.'), ('languages_gui.json', '.'), ('languages_inputfile.json', '.'), ('languages_months.json', '.'), ('languages_output.json', '.')],
    hiddenimports=['scipy.special._cdflib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='splitwise_plotter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
