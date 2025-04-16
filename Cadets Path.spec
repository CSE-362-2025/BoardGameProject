# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py', 'database.py', 'event.py', 'game_manager.py', 'llm_model.py', 'player.py', 'tests.py', 'tiles.py', 'ui.py'],
    pathex=[],
    binaries=[],
    datas=[('.', '.'), ('Resources', 'Resources'), ('game_objects', 'game_objects'), ('database', 'database')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Cadets Path',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon="Resources/monkeyhat.ico",
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
