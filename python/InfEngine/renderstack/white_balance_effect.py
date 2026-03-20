"""
WhiteBalanceEffect — Color temperature and tint adjustment.

Aligned with Unity URP White Balance. Operates in HDR space
(before_post_process) using Bradford chromatic adaptation.

Parameters:
    temperature — warm/cool shift (-100 to 100, 0 = neutral)
    tint        — green/magenta shift (-100 to 100, 0 = neutral)
"""

from __future__ import annotations

from typing import List, TYPE_CHECKING

from InfEngine.renderstack.fullscreen_effect import FullScreenEffect
from InfEngine.components.serialized_field import serialized_field

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import RenderGraph
    from InfEngine.renderstack.resource_bus import ResourceBus


class WhiteBalanceEffect(FullScreenEffect):
    """URP-aligned White Balance post-processing effect."""

    name = "White Balance"
    injection_point = "before_post_process"
    default_order = 150
    menu_path = "Post-processing/White Balance"

    temperature: float = serialized_field(default=0.0, range=(-100.0, 100.0), slider=False)
    tint: float = serialized_field(default=0.0, range=(-100.0, 100.0), slider=False)

    def get_shader_list(self) -> List[str]:
        return ["fullscreen_triangle", "white_balance"]

    def setup_passes(self, graph: "RenderGraph", bus: "ResourceBus") -> None:
        from InfEngine.rendergraph.graph import Format

        color_in = bus.get("color")
        if color_in is None:
            return

        _tex = self.get_or_create_texture

        color_out = _tex(graph, "_whitebal_out", format=Format.RGBA16_SFLOAT)

        with graph.add_pass("WhiteBal_Apply") as p:
            p.set_texture("_SourceTex", color_in)
            p.write_color(color_out)
            p.set_param("temperature", self.temperature)
            p.set_param("tint", self.tint)
            p.fullscreen_quad("white_balance")

        bus.set("color", color_out)
