"""
ChromaticAberrationEffect — RGB channel separation from screen center.

Aligned with Unity URP Chromatic Aberration. Simulates lens imperfection
where different wavelengths refract at different angles.

Parameters:
    intensity — channel separation strength (0 = off, 1 = strong)
"""

from __future__ import annotations

from typing import List, TYPE_CHECKING

from InfEngine.renderstack.fullscreen_effect import FullScreenEffect
from InfEngine.components.serialized_field import serialized_field

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import RenderGraph
    from InfEngine.renderstack.resource_bus import ResourceBus


class ChromaticAberrationEffect(FullScreenEffect):
    """URP-aligned Chromatic Aberration post-processing effect."""

    name = "Chromatic Aberration"
    injection_point = "before_post_process"
    default_order = 600
    menu_path = "Post-processing/Chromatic Aberration"

    intensity: float = serialized_field(default=0.1, range=(0.0, 1.0), slider=False)

    def get_shader_list(self) -> List[str]:
        return ["fullscreen_triangle", "chromatic_aberration"]

    def setup_passes(self, graph: "RenderGraph", bus: "ResourceBus") -> None:
        from InfEngine.rendergraph.graph import Format

        color_in = bus.get("color")
        if color_in is None:
            return

        _tex = self.get_or_create_texture

        color_out = _tex(graph, "_chromab_out", format=Format.RGBA16_SFLOAT)

        with graph.add_pass("ChromAb_Apply") as p:
            p.set_texture("_SourceTex", color_in)
            p.write_color(color_out)
            p.set_param("intensity", self.intensity)
            p.fullscreen_quad("chromatic_aberration")

        bus.set("color", color_out)
