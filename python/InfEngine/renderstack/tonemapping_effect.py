"""
ToneMappingEffect — HDR-to-LDR tone mapping post-processing effect.

Maps linear HDR scene color into displayable LDR range. Should be the
last effect in the post-process stack (runs at ``after_post_process``)
so that bloom and other HDR effects are applied first.

Supported operators:
    - Reinhard
    - ACES Filmic (default — matches Unity/Unreal look)
"""

from __future__ import annotations

from enum import IntEnum
from typing import List, TYPE_CHECKING

from InfEngine.renderstack.fullscreen_effect import FullScreenEffect
from InfEngine.components.serialized_field import serialized_field

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import RenderGraph
    from InfEngine.renderstack.resource_bus import ResourceBus


class ToneMappingMode(IntEnum):
    """Tone mapping operator."""
    None_    = 0
    Reinhard = 1
    ACES     = 2


class ToneMappingEffect(FullScreenEffect):
    """HDR-to-LDR tone mapping post-processing effect.

    Should be the last effect in the post-process chain so that bloom
    and other HDR effects can operate on the full dynamic range.
    """

    name = "Tone Mapping"
    injection_point = "after_post_process"
    default_order = 900          # high order → runs last within its injection point
    menu_path = "Post-processing/Tone Mapping"

    # ---- Serialized parameters (shown in Inspector) ----
    mode: ToneMappingMode = serialized_field(
        default=ToneMappingMode.ACES,
        tooltip="Tone mapping operator (ACES is recommended for realistic look)",
    )
    exposure: float = serialized_field(
        default=1.0,
        range=(0.01, 10.0),
        drag_speed=0.05,
        slider=False,
        tooltip="Pre-tonemap exposure multiplier",
    )
    gamma: float = serialized_field(
        default=2.2,
        range=(1.0, 3.0),
        drag_speed=0.01,
        slider=False,
        tooltip="Gamma correction exponent (2.2 = standard sRGB)",
    )
    @staticmethod
    def _normalize_mode_value(value) -> ToneMappingMode:
        """Map legacy serialized values onto supported operators."""
        if isinstance(value, ToneMappingMode):
            return value
        if isinstance(value, dict):
            enum_name = value.get("__enum_name__", "")
            if enum_name == "NONE":
                return ToneMappingMode.None_
            if enum_name in ToneMappingMode.__members__:
                return ToneMappingMode[enum_name]
        if value == 0:
            return ToneMappingMode.None_
        try:
            return ToneMappingMode(int(value))
        except (ValueError, KeyError):
            return ToneMappingMode.ACES

    def set_params_dict(self, params):
        super().set_params_dict(params)
        self.mode = self._normalize_mode_value(params.get("mode", self.mode))

    # ------------------------------------------------------------------
    # FullScreenEffect interface
    # ------------------------------------------------------------------

    def get_shader_list(self) -> List[str]:
        return [
            "fullscreen_triangle",
            "tonemapping",
        ]

    def setup_passes(self, graph: "RenderGraph", bus: "ResourceBus") -> None:
        """Inject the tonemapping pass into the render graph."""
        color_in = bus.get("color")
        if color_in is None:
            return

        from InfEngine.rendergraph.graph import Format

        _tex = self.get_or_create_texture

        color_out = _tex(graph, "_tonemap_out", format=Format.RGBA16_SFLOAT)

        with graph.add_pass("ToneMap_Apply") as p:
            p.set_texture("_SourceTex", color_in)
            p.write_color(color_out)
            mode = self._normalize_mode_value(self.mode)
            self.mode = mode
            p.set_param("mode", float(int(mode)))
            p.set_param("exposure", self.exposure)
            p.set_param("gamma", self.gamma)
            p.fullscreen_quad("tonemapping")

        bus.set("color", color_out)
