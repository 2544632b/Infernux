"""
SharpenEffect — Contrast Adaptive Sharpening (CAS) post-processing effect.

Implements AMD FidelityFX CAS-inspired sharpening. Enhances local contrast
without introducing visible halos. Operates in LDR space (after_post_process)
after tone mapping, matching the typical game sharpening pipeline placement.

Parameters:
    intensity — sharpening strength (0 = off, 1 = maximum sharpening)
"""

from __future__ import annotations

from typing import List, TYPE_CHECKING

from InfEngine.renderstack.fullscreen_effect import FullScreenEffect
from InfEngine.components.serialized_field import serialized_field

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import RenderGraph
    from InfEngine.renderstack.resource_bus import ResourceBus


class SharpenEffect(FullScreenEffect):
    """Contrast Adaptive Sharpening (CAS) post-processing effect.

    Placed after tone mapping to sharpen the final LDR image.
    Based on AMD FidelityFX CAS algorithm.
    """

    name = "Sharpen"
    injection_point = "after_post_process"
    default_order = 850  # after film grain (800), before final output
    menu_path = "Post-processing/Sharpen"

    # ---- Serialized parameters ----
    intensity: float = serialized_field(
        default=0.5,
        range=(0.0, 1.0),
        drag_speed=0.01,
        slider=False,
        tooltip="Sharpening strength (0 = off, 1 = maximum)",
    )

    # ------------------------------------------------------------------
    # FullScreenEffect interface
    # ------------------------------------------------------------------

    def get_shader_list(self) -> List[str]:
        return ["fullscreen_triangle", "sharpen_cas"]

    def setup_passes(self, graph: "RenderGraph", bus: "ResourceBus") -> None:
        from InfEngine.rendergraph.graph import Format

        color_in = bus.get("color")
        if color_in is None:
            return

        _tex = self.get_or_create_texture

        color_out = _tex(graph, "_sharpen_out", format=Format.RGBA16_SFLOAT)

        with graph.add_pass("Sharpen_CAS") as p:
            p.set_texture("_SourceTex", color_in)
            p.write_color(color_out)
            p.set_param("intensity", self.intensity)
            p.fullscreen_quad("sharpen_cas")

        bus.set("color", color_out)
