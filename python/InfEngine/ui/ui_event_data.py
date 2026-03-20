"""Pointer event data — carries context for all UI pointer callbacks.

Mirrors Unity's ``PointerEventData`` but simplified for InfEngine's
pure screen-space UI.  Passed to ``on_pointer_enter``, ``on_pointer_click``,
etc. on any ``InfUIScreenComponent`` subclass.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from InfEngine.ui.inf_ui_screen_component import InfUIScreenComponent
    from InfEngine.ui.ui_canvas import UICanvas


class PointerButton(IntEnum):
    """Mouse button index (matches SDL / Input.get_mouse_button)."""
    Left = 0
    Right = 1
    Middle = 2


class PointerEventData:
    """Data container for a single pointer event.

    Attributes:
        position: Current pointer position in *canvas design* pixels.
        delta: Frame-to-frame delta in canvas design pixels.
        button: Which mouse button triggered this event.
        press_position: Canvas-space position where the button was pressed.
        click_count: Number of rapid clicks (1 = single, 2 = double, …).
        canvas: The ``UICanvas`` owning the target element.
        target: The ``InfUIScreenComponent`` this event is addressed to.
        used: Set to ``True`` in a handler to stop further propagation.
    """

    __slots__ = (
        "position", "delta", "button",
        "press_position", "click_count",
        "scroll_delta",
        "canvas", "target", "used",
    )

    def __init__(self):
        self.position: Tuple[float, float] = (0.0, 0.0)
        self.delta: Tuple[float, float] = (0.0, 0.0)
        self.button: PointerButton = PointerButton.Left
        self.press_position: Tuple[float, float] = (0.0, 0.0)
        self.click_count: int = 0
        self.scroll_delta: Tuple[float, float] = (0.0, 0.0)
        self.canvas: Optional[UICanvas] = None
        self.target: Optional[InfUIScreenComponent] = None
        self.used: bool = False

    def Use(self):
        """Mark event as consumed (stops propagation to parent elements)."""
        self.used = True
