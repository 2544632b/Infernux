"""Utility helpers shared across the Hub codebase."""

import sys


def is_frozen() -> bool:
    """Return *True* when running inside a PyInstaller bundle."""
    return getattr(sys, "frozen", False)
