import json
import os
from typing import Optional

_project_root: Optional[str] = None
_guid_manifest: Optional[dict] = None
_guid_manifest_loaded: bool = False


def set_project_root(path: Optional[str]) -> None:
    """Set the current project root for path normalization."""
    global _project_root
    _project_root = os.path.abspath(path) if path else None


def get_project_root() -> Optional[str]:
    """Get the current project root if set."""
    return _project_root


def resolve_script_path(path: Optional[str]) -> Optional[str]:
    """Resolve a possibly relative script path to an absolute path.

    In packaged builds the original ``.py`` sources are compiled to
    ``.pyc`` and removed.  If the resolved ``.py`` path does not exist
    but a corresponding ``.pyc`` does, the ``.pyc`` path is returned
    so that callers transparently load the compiled version.
    """
    if not path:
        return path
    if os.path.isabs(path):
        resolved = path
    elif _project_root:
        resolved = os.path.abspath(os.path.join(_project_root, path))
    else:
        resolved = os.path.abspath(path)

    # Fallback: .py → .pyc for packaged builds
    if not os.path.exists(resolved) and resolved.endswith('.py'):
        pyc = resolved + 'c'
        if os.path.exists(pyc):
            return pyc
    return resolved


def resolve_guid_to_path(guid: str) -> Optional[str]:
    """Resolve a script GUID using the build-time manifest.

    In packaged builds the original ``.py`` sources are compiled to
    ``.pyc`` and removed.  The C++ ``AssetDatabase`` cannot register
    ``.pyc`` files, so GUID look-ups return empty.  At build time a
    ``_script_guid_map.json`` manifest is written that maps GUIDs to
    relative ``.pyc`` paths.  This function loads and queries it.
    """
    global _guid_manifest, _guid_manifest_loaded
    if not _guid_manifest_loaded:
        _guid_manifest_loaded = True
        if _project_root:
            manifest = os.path.join(_project_root, "_script_guid_map.json")
            if os.path.isfile(manifest):
                try:
                    with open(manifest, "r", encoding="utf-8") as f:
                        _guid_manifest = json.load(f)
                except (json.JSONDecodeError, OSError):
                    pass
    if _guid_manifest and guid and guid in _guid_manifest:
        rel = _guid_manifest[guid]
        if _project_root:
            return os.path.join(_project_root, rel)
    return None
