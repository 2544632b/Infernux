"""
FilmGrainEffect — Cinematic noise overlay.

Aligned with Unity URP Film Grain (simplified white noise type).
Operates in LDR space (after_post_process) to match URP behaviour
where grain is applied after tone mapping.

Parameters:
    intensity — grain strength (0 = off, 1 = heavy)
    response  — luminance response (0 = uniform, 1 = highlights only)
"""

from __future__ import annotations

import time as _time
from typing import List, TYPE_CHECKING

from InfEngine.renderstack.fullscreen_effect import FullScreenEffect
from InfEngine.components.serialized_field import serialized_field

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import RenderGraph
    from InfEngine.renderstack.resource_bus import ResourceBus


class FilmGrainEffect(FullScreenEffect):
    """URP-aligned Film Grain post-processing effect."""

    name = "Film Grain"
    injection_point = "after_post_process"
    default_order = 800
    menu_path = "Post-processing/Film Grain"

    intensity: float = serialized_field(default=0.2, range=(0.0, 1.0), slider=False)
    response: float = serialized_field(default=0.8, range=(0.0, 1.0), slider=False)

    def get_shader_list(self) -> List[str]:
        return ["fullscreen_triangle", "film_grain"]

    def setup_passes(self, graph: "RenderGraph", bus: "ResourceBus") -> None:
        from InfEngine.rendergraph.graph import Format

        color_in = bus.get("color")
        if color_in is None:
            return

        _tex = self.get_or_create_texture

        color_out = _tex(graph, "_filmgrain_out", format=Format.RGBA16_SFLOAT)

        with graph.add_pass("FilmGrain_Apply") as p:
            p.set_texture("_SourceTex", color_in)
            p.write_color(color_out)
            p.set_param("intensity", self.intensity)
            p.set_param("response", self.response)
            p.set_param("time", float(_time.perf_counter() % 1000.0))
            p.fullscreen_quad("film_grain")

        bus.set("color", color_out)
