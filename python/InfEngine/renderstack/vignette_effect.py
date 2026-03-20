"""
VignetteEffect — Darkens screen edges for cinematic framing.

Aligned with Unity URP Vignette. Runs in HDR space (before_post_process)
so that tone mapping applies to the vignetted result.

Parameters:
    intensity   — vignette strength (0 = off, 1 = full black edges)
    smoothness  — falloff softness
    roundness   — shape control (1 = circular, lower = squared)
    rounded     — force perfectly circular regardless of aspect ratio
"""

from __future__ import annotations

from typing import List, TYPE_CHECKING

from InfEngine.renderstack.fullscreen_effect import FullScreenEffect
from InfEngine.components.serialized_field import serialized_field

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import RenderGraph
    from InfEngine.renderstack.resource_bus import ResourceBus


class VignetteEffect(FullScreenEffect):
    """URP-aligned Vignette post-processing effect."""

    name = "Vignette"
    injection_point = "before_post_process"
    default_order = 500
    menu_path = "Post-processing/Vignette"

    intensity: float = serialized_field(default=0.35, range=(0.0, 1.0), slider=False)
    smoothness: float = serialized_field(default=0.3, range=(0.01, 1.0), slider=False)
    roundness: float = serialized_field(default=1.0, range=(0.0, 1.0), slider=False)
    rounded: bool = serialized_field(default=False)

    def get_shader_list(self) -> List[str]:
        return ["fullscreen_triangle", "vignette"]

    def setup_passes(self, graph: "RenderGraph", bus: "ResourceBus") -> None:
        from InfEngine.rendergraph.graph import Format

        color_in = bus.get("color")
        if color_in is None:
            return

        _tex = self.get_or_create_texture

        color_out = _tex(graph, "_vignette_out", format=Format.RGBA16_SFLOAT)

        with graph.add_pass("Vignette_Apply") as p:
            p.set_texture("_SourceTex", color_in)
            p.write_color(color_out)
            p.set_param("intensity", self.intensity)
            p.set_param("smoothness", self.smoothness)
            p.set_param("roundness", self.roundness)
            p.set_param("rounded", 1.0 if self.rounded else 0.0)
            p.fullscreen_quad("vignette")

        bus.set("color", color_out)
