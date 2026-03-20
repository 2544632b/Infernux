"""Shared canvas-discovery utilities for the UI system.

Avoids duplicating the recursive canvas-collection logic across
UIEditorPanel and GameViewPanel.
"""

from __future__ import annotations

from operator import attrgetter
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    pass  # avoid circular imports at runtime

_sort_key = attrgetter('sort_order')

# ── Cached canvas collection ────────────────────────────────────────
# Avoids a full DFS every frame; rebuilt only when scene structure changes.
_canvas_cache: list = []
_canvas_sorted_cache: list = []
_canvas_with_go_cache: list = []
_canvas_cache_version: int = -1


def _rebuild_cache(scene) -> None:
    global _canvas_cache, _canvas_sorted_cache, _canvas_with_go_cache, _canvas_cache_version
    from InfEngine.ui import UICanvas

    result: list = []

    def _walk(go):
        for comp in go.get_py_components():
            if isinstance(comp, UICanvas):
                result.append((go, comp))
        for child in go.get_children():
            _walk(child)

    if scene is not None:
        for root in scene.get_root_objects():
            _walk(root)

    _canvas_with_go_cache = result
    _canvas_cache = [comp for _, comp in result]
    _canvas_sorted_cache = sorted(_canvas_cache, key=_sort_key)
    _canvas_cache_version = scene.structure_version if scene is not None else -1


def invalidate_canvas_cache() -> None:
    """Force cache invalidation (e.g. on scene load)."""
    global _canvas_cache_version
    _canvas_cache_version = -1


def collect_canvases_with_go(scene) -> List[Tuple]:
    """Return ``[(GameObject, UICanvas), ...]`` for every canvas in *scene*.

    Walks the full scene hierarchy.  Used by UIEditorPanel which needs
    both the owning GameObject and the canvas component.
    """
    global _canvas_cache_version
    if scene is None:
        return []
    ver = scene.structure_version
    if ver != _canvas_cache_version:
        _rebuild_cache(scene)
    return _canvas_with_go_cache


def collect_canvases(scene) -> list:
    """Return ``[UICanvas, ...]`` for every canvas in *scene*.

    Lighter variant used by GameViewPanel which only needs the component.
    """
    global _canvas_cache_version
    if scene is None:
        return []
    ver = scene.structure_version
    if ver != _canvas_cache_version:
        _rebuild_cache(scene)
    return _canvas_cache


def collect_sorted_canvases(scene) -> list:
    """Return ``[UICanvas, ...]`` sorted by ``sort_order`` (cached)."""
    global _canvas_cache_version
    if scene is None:
        return []
    ver = scene.structure_version
    if ver != _canvas_cache_version:
        _rebuild_cache(scene)
    return _canvas_sorted_cache
