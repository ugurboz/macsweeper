"""Setup script for building the MacSweeper Pro macOS App using py2app."""
from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('ui/web', ['ui/web/index.html', 'ui/web/script.js', 'ui/web/style.css']),
    ('ui/web/assets', ['ui/web/assets/icon.png']),
]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'assets/macsweeper.icns',
    'plist': {
        'CFBundleName': 'MacSweeper Pro',
        'CFBundleDisplayName': 'MacSweeper Pro',
        'CFBundleGetInfoString': 'A premium system cleaner for macOS',
        'CFBundleIdentifier': 'com.ugurboz.macsweeper',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2026 Ugur Boz. All Rights Reserved.',
        'LSMinimumSystemVersion': '10.15',
        'NSHighResolutionCapable': True,
    },
    'packages': ['webview'],
    'includes': ['PIL', 'PIL._tkinter_finder', 'PIL._imaging', 'PIL._imagingmath', 'PIL._imagingtk', 'PIL._imagingmorph', 'PIL._avif', 'PIL._webp'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
