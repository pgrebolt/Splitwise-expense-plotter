# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['your_script.py'],
    pathex=['/path/to/your/script'],
    binaries=[],
    datas=[
        ('additional_file1.py', '.'),  # Include additional_file1.py in the same directory as the executable
        ('additional_file2.py', '.'),  # Include additional_file2.py in the same directory as the executable
        ('resources/', 'resources/'),  # Include the resources directory and its contents
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='your_program_name',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want a console window
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='your_program_name',
)