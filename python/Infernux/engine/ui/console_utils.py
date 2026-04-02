"""Shared console/log-entry utilities.

Extracted from the old Python ``ConsolePanel`` so that both
``bootstrap.py`` (StatusBar wiring) and any future consumer can
use them without importing a heavy panel module.
"""
from __future__ import annotations


def sanitize_text(value) -> str:
    """Normalize arbitrary text into a UI-safe UTF-8 string."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        text = value.decode("utf-8", errors="replace")
    else:
        text = str(value)
    text = text.replace("\x00", "\ufffd")
    return text.encode("utf-8", errors="replace").decode("utf-8", errors="replace")


def is_internal(entry) -> bool:
    """Return True if *entry* is internal engine noise.

    Checks the ``internal`` flag set at the source via
    ``Debug.log_internal()``.  Also filters Dear ImGui programmer
    errors that leak through the C++ layer.
    """
    if getattr(entry, "internal", False):
        return True
    msg = entry.message if hasattr(entry, "message") else str(entry)
    if "DEAR IMGUI" in msg or "PushID" in msg or "conflicting ID" in msg:
        return True
    return False
