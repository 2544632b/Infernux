"""Resource paths for InfEngine Hub (launcher).

Resolves to packaging/resources/ whether running from source or
from a PyInstaller frozen bundle.
"""

import os
import sys


def _resource_dir() -> str:
    if getattr(sys, "frozen", False):
        # PyInstaller puts data files in sys._MEIPASS
        return os.path.join(sys._MEIPASS, "resources")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")


RESOURCE_DIR = _resource_dir()
ICON_PATH = os.path.join(RESOURCE_DIR, "icon.png")
FONT_PATH = os.path.join(RESOURCE_DIR, "PingFangTC-Regular.otf")
