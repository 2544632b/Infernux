"""UICanvas — root container for screen-space UI elements.

A UICanvas is attached to a GameObject in the Hierarchy.
All UI elements (UIText, etc.) are children of the Canvas's GameObject.
The Canvas itself only stores configuration; rendering is handled by
the UI Editor panel & Game View overlay via ImGui draw primitives.

The canvas defines a *design* reference resolution (default 1920×1080).
At runtime the Game View scales from design resolution to actual viewport
size so that all positions, sizes and font sizes adapt proportionally.

Hierarchy:
    InfComponent → InfUIComponent → UICanvas
"""

from InfEngine.components import (
    disallow_multiple,
    add_component_menu,
    serialized_field,
    int_field,
)
from .inf_ui_component import InfUIComponent
from .enums import RenderMode


@disallow_multiple
@add_component_menu("UI/Canvas")
class UICanvas(InfUIComponent):
    """Screen-space UI canvas.

    reference_width / reference_height are the *design* reference resolution.
    They are user-editable and default to 1920×1080.  At runtime the Game
    View overlay scales all element positions, sizes and font sizes
    proportionally from this reference to the actual viewport.

    Attributes:
        render_mode: ScreenOverlay or CameraOverlay.
        sort_order: Rendering order (lower draws first).
        target_camera_id: Camera GameObject ID (CameraOverlay mode only).
    """

    render_mode: RenderMode = serialized_field(default=RenderMode.ScreenOverlay)
    sort_order: int = int_field(0, range=(-1000, 1000), tooltip="Render order (lower = earlier)")
    target_camera_id: int = int_field(0, tooltip="Camera ID for CameraOverlay mode")

    # Design reference resolution (serialized, user-editable)
    reference_width: int = int_field(1920, range=(1, 8192), tooltip="Design reference width", slider=False)
    reference_height: int = int_field(1080, range=(1, 8192), tooltip="Design reference height", slider=False)

    # ------------------------------------------------------------------
    # Cached element list (invalidated when hierarchy changes)
    # ------------------------------------------------------------------
    _cached_elements: list = None
    _cached_elements_version: int = -1

    def invalidate_element_cache(self):
        """Mark the cached element list as stale.

        Called automatically when structure_version changes.
        Also call manually after hierarchy changes (add/remove children).
        """
        self._cached_elements = None

    def _get_elements(self):
        """Return the cached element list, rebuilding if necessary.

        Uses scene.structure_version to avoid DFS every frame.
        """
        go = self.game_object
        if go is not None:
            scene = go.scene
            if scene is not None:
                ver = scene.structure_version
                if ver != self._cached_elements_version:
                    self._cached_elements = None
                    self._cached_elements_version = ver
        if self._cached_elements is None:
            self._cached_elements = list(self.iter_ui_elements())
        return self._cached_elements

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def iter_ui_elements(self):
        """Yield all screen-space UI components on child GameObjects (depth-first)."""
        go = self.game_object
        if go is None:
            return
        yield from self._walk_children(go)

    def _walk_children(self, parent):
        from .inf_ui_screen_component import InfUIScreenComponent
        for child in parent.get_children():
            for comp in child.get_py_components():
                if isinstance(comp, InfUIScreenComponent):
                    yield comp
            yield from self._walk_children(child)

    def raycast(self, canvas_x: float, canvas_y: float):
        """Return the front-most element hit at (canvas_x, canvas_y), or None.

        Iterates children in reverse depth-first order (last drawn = top).
        Only elements with ``raycast_target = True`` participate.
        Uses AABB pre-rejection before the full rotated hit-test.
        """
        ref_w = float(self.reference_width)
        ref_h = float(self.reference_height)
        elements = self._get_elements()
        for elem in reversed(elements):
            if not getattr(elem, "raycast_target", True):
                continue
            if not getattr(elem, "enabled", True):
                continue
            # AABB pre-rejection: skip expensive contains_point if outside visual rect
            vx, vy, vw, vh = elem.get_visual_rect(ref_w, ref_h)
            if not (vx <= canvas_x <= vx + vw and vy <= canvas_y <= vy + vh):
                continue
            if elem.contains_point(canvas_x, canvas_y, ref_w, ref_h):
                return elem
        return None

    def raycast_all(self, canvas_x: float, canvas_y: float):
        """Return all elements hit at (canvas_x, canvas_y), front-to-back order."""
        ref_w = float(self.reference_width)
        ref_h = float(self.reference_height)
        elements = self._get_elements()
        hits = []
        for elem in reversed(elements):
            if not getattr(elem, "raycast_target", True):
                continue
            if not getattr(elem, "enabled", True):
                continue
            # AABB pre-rejection
            vx, vy, vw, vh = elem.get_visual_rect(ref_w, ref_h)
            if not (vx <= canvas_x <= vx + vw and vy <= canvas_y <= vy + vh):
                continue
            if elem.contains_point(canvas_x, canvas_y, ref_w, ref_h):
                hits.append(elem)
        return hits
