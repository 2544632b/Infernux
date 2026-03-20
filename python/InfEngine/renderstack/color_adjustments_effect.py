"""
ColorAdjustmentsEffect — Post-exposure, contrast, saturation, hue shift.

Aligned with Unity URP Color Adjustments. Operates in HDR space
(before_post_process) so adjustments apply before tone mapping.

Parameters:
    post_exposure — exposure offset in EV stops
    contrast      — contrast adjustment (-100 to 100)
    saturation    — saturation adjustment (-100 to 100)
    hue_shift     — hue rotation in degrees (-180 to 180)
"""

from __future__ import annotations

from typing import List, TYPE_CHECKING

from InfEngine.renderstack.fullscreen_effect import FullScreenEffect
from InfEngine.components.serialized_field import serialized_field

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import RenderGraph
    from InfEngine.renderstack.resource_bus import ResourceBus


class ColorAdjustmentsEffect(FullScreenEffect):
    """URP-aligned Color Adjustments post-processing effect."""

    name = "Color Adjustments"
    injection_point = "before_post_process"
    default_order = 200
    menu_path = "Post-processing/Color Adjustments"

    post_exposure: float = serialized_field(default=0.0, range=(-5.0, 5.0), drag_speed=0.05, slider=False)
    contrast: float = serialized_field(default=0.0, range=(-100.0, 100.0), slider=False)
    saturation: float = serialized_field(default=0.0, range=(-100.0, 100.0), slider=False)
    hue_shift: float = serialized_field(default=0.0, range=(-180.0, 180.0), slider=False)

    def get_shader_list(self) -> List[str]:
        return ["fullscreen_triangle", "color_adjustments"]

    def setup_passes(self, graph: "RenderGraph", bus: "ResourceBus") -> None:
        from InfEngine.rendergraph.graph import Format

        color_in = bus.get("color")
        if color_in is None:
            return

        _tex = self.get_or_create_texture

        color_out = _tex(graph, "_coloradj_out", format=Format.RGBA16_SFLOAT)

        with graph.add_pass("ColorAdj_Apply") as p:
            p.set_texture("_SourceTex", color_in)
            p.write_color(color_out)
            p.set_param("postExposure", self.post_exposure)
            p.set_param("contrast", self.contrast)
            p.set_param("saturation", self.saturation)
            p.set_param("hueShift", self.hue_shift)
            p.fullscreen_quad("color_adjustments")

        bus.set("color", color_out)
