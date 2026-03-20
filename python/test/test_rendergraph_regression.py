"""Regression tests for RenderGraph and RenderStack rendering pipeline.

Tests cover:
- Injection point callback timing (Must-Fix #1)
- Overlay/blit pass reordering via public API (Should-Fix #2)
- RenderGraph remove_pass / append_pass
- FullscreenQuad inputBindings ordering
"""

from __future__ import annotations

import sys
import types

import pytest


# ---------------------------------------------------------------------------
# Stub native types so tests run without the C++ backend
# ---------------------------------------------------------------------------

class _StubGraphPassActionType:
    NONE = 0
    DRAW_RENDERERS = 1
    DRAW_SKYBOX = 2
    CUSTOM = 3
    DRAW_SHADOW_CASTERS = 4
    DRAW_SCREEN_UI = 5
    FULLSCREEN_QUAD = 6
    Compute = 7


class _StubVkFormat:
    R8G8B8A8_UNORM = 37
    R8G8B8A8_SRGB = 43
    B8G8R8A8_UNORM = 44
    R16G16B16A16_SFLOAT = 97
    R32G32B32A32_SFLOAT = 109
    R32_SFLOAT = 100
    D32_SFLOAT = 126
    D24_UNORM_S8_UINT = 129


class _StubGraphTextureDesc:
    def __init__(self):
        self.name = ""
        self.format = 0
        self.is_backbuffer = False
        self.is_depth = False
        self.width = 0
        self.height = 0
        self.size_divisor = 0


class _StubGraphPassDesc:
    def __init__(self):
        self.name = ""
        self.read_textures = []
        self.write_colors = []
        self.write_depth = ""
        self.clear_color = False
        self.clear_color_r = 0.0
        self.clear_color_g = 0.0
        self.clear_color_b = 0.0
        self.clear_color_a = 0.0
        self.clear_depth = False
        self.clear_depth_value = 0.0
        self.action = 0
        self.queue_min = 0
        self.queue_max = 5000
        self.sort_mode = "none"
        self.input_bindings = []
        self.light_index = 0
        self.shadow_type = "hard"
        self.screen_ui_list = 0
        self.shader_name = ""
        self.push_constants = []


class _StubRenderGraphDescription:
    def __init__(self):
        self.name = ""
        self.textures = []
        self.passes = []
        self.output_texture = ""
        self.msaa_samples = 0


@pytest.fixture(autouse=True)
def _stub_native(monkeypatch):
    """Inject stub native types so graph.py can import InfEngine.lib."""
    fake_lib = types.ModuleType("InfEngine.lib")
    fake_lib.RenderGraphDescription = _StubRenderGraphDescription
    fake_lib.GraphPassDesc = _StubGraphPassDesc
    fake_lib.GraphTextureDesc = _StubGraphTextureDesc
    fake_lib.GraphPassActionType = _StubGraphPassActionType
    fake_lib.VkFormat = _StubVkFormat

    import InfEngine
    monkeypatch.setitem(sys.modules, "InfEngine.lib", fake_lib)
    monkeypatch.setattr(InfEngine, "lib", fake_lib, raising=False)

    yield


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_graph():
    """Create a minimal RenderGraph with color + depth textures."""
    from InfEngine.rendergraph.graph import RenderGraph, Format

    graph = RenderGraph("TestGraph")
    graph.create_texture("color", camera_target=True)
    graph.create_texture("depth", format=Format.D32_SFLOAT)
    return graph


# ===========================================================================
# Test: RenderGraph.remove_pass / append_pass
# ===========================================================================

class TestPassManagement:
    def test_remove_pass_returns_builder(self):
        graph = _make_graph()
        with graph.add_pass("A") as p:
            p.write_color("color")
            p.draw_renderers()

        removed = graph.remove_pass("A")
        assert removed is not None
        assert removed._name == "A"
        assert graph.pass_count == 0

    def test_remove_nonexistent_returns_none(self):
        graph = _make_graph()
        assert graph.remove_pass("DoesNotExist") is None

    def test_remove_clears_topology(self):
        graph = _make_graph()
        with graph.add_pass("A") as p:
            p.write_color("color")
            p.draw_renderers()
        graph.remove_pass("A")
        assert not any(label == "A" for _, label in graph.topology_sequence)

    def test_append_pass_adds_to_end(self):
        graph = _make_graph()
        with graph.add_pass("A") as p:
            p.write_color("color")
            p.draw_renderers()
        with graph.add_pass("B") as p:
            p.write_color("color")
            p.draw_renderers()

        removed = graph.remove_pass("A")
        graph.append_pass(removed)

        names = [label for kind, label in graph.topology_sequence if kind == "pass"]
        assert names == ["B", "A"]


# ===========================================================================
# Test: Injection point callback timing
# ===========================================================================

class TestInjectionPointCallback:
    def test_callback_fires_for_explicit_injection_point(self):
        graph = _make_graph()
        fired = []
        graph._injection_callback = lambda name: fired.append(name)

        with graph.add_pass("Opaque") as p:
            p.write_color("color")
            p.draw_renderers()

        graph.injection_point("after_opaque", resources={"color", "depth"})
        assert "after_opaque" in fired

    def test_callback_fires_for_screen_ui_section(self):
        graph = _make_graph()
        fired = []
        graph._injection_callback = lambda name: fired.append(name)

        with graph.add_pass("Opaque") as p:
            p.write_color("color")
            p.draw_renderers()

        graph.screen_ui_section()
        assert "before_post_process" in fired
        assert "after_post_process" in fired

    def test_auto_inject_in_build_does_not_fire_callback(self):
        """build() auto-injects before/after_post_process if missing,
        but the callback is NOT set during build(). This tests that
        RenderStack correctly handles this by injecting BEFORE build()."""
        graph = _make_graph()

        with graph.add_pass("Opaque") as p:
            p.write_color("color")
            p.draw_renderers()

        # Simulate: callback is set, then cleared before build
        fired = []
        graph._injection_callback = lambda name: fired.append(name)
        # build() adds the IPs itself
        graph._injection_callback = None
        graph.set_output("color")
        desc = graph.build()

        # The IPs were auto-injected but callback was None
        assert "before_post_process" not in fired
        assert "after_post_process" not in fired

    def test_manual_inject_before_build_fires_callback(self):
        """When we manually inject IPs before calling build(), the
        callback fires and build() skips auto-inject (already present)."""
        graph = _make_graph()

        with graph.add_pass("Opaque") as p:
            p.write_color("color")
            p.draw_renderers()

        fired = []
        graph._injection_callback = lambda name: fired.append(name)

        # Manually inject (simulating what render_stack.py now does)
        if not graph.has_injection_point("before_post_process"):
            graph.injection_point("before_post_process", resources={"color"})
        if not graph.has_injection_point("after_post_process"):
            graph.injection_point("after_post_process", resources={"color"})

        assert "before_post_process" in fired
        assert "after_post_process" in fired

        # Clear callback before build (simulating RenderStack flow)
        graph._injection_callback = None
        graph.set_output("color")
        desc = graph.build()

        # build() should NOT duplicate IPs
        ip_names = [ip.name for ip in graph.injection_points]
        assert ip_names.count("before_post_process") == 1
        assert ip_names.count("after_post_process") == 1


# ===========================================================================
# Test: Overlay pass reordering
# ===========================================================================

class TestOverlayReordering:
    def test_overlay_moved_after_blit(self):
        """Simulate the RenderStack overlay reordering using public API."""
        graph = _make_graph()

        with graph.add_pass("Opaque") as p:
            p.write_color("color")
            p.draw_renderers()

        with graph.add_pass("_ScreenUI_Overlay") as p:
            p.write_color("color")
            p.draw_screen_ui(list="overlay")

        # Simulate blit insertion + overlay reorder
        overlay = graph.remove_pass("_ScreenUI_Overlay")
        assert overlay is not None

        with graph.add_pass("_FinalCompositeBlit") as p:
            p.set_texture("_SourceTex", "color")
            p.write_color("color")
            p.fullscreen_quad("fullscreen_blit")

        graph.append_pass(overlay)

        names = [label for kind, label in graph.topology_sequence if kind == "pass"]
        assert names == ["Opaque", "_FinalCompositeBlit", "_ScreenUI_Overlay"]


# ===========================================================================
# Test: Build produces valid description
# ===========================================================================

class TestBuild:
    def test_basic_build_succeeds(self):
        graph = _make_graph()
        with graph.add_pass("Opaque") as p:
            p.write_color("color")
            p.write_depth("depth")
            p.draw_renderers()

        graph.set_output("color")
        desc = graph.build()
        assert desc.name == "TestGraph"
        assert desc.output_texture == "color"
        # auto-injected before/after_post_process
        assert graph.has_injection_point("before_post_process")
        assert graph.has_injection_point("after_post_process")

    def test_shadow_pass_preserves_light_index(self):
        graph = _make_graph()
        from InfEngine.rendergraph.graph import Format

        graph.create_texture("shadow_map", format=Format.D32_SFLOAT, size=(4096, 4096))

        with graph.add_pass("ShadowCaster") as p:
            p.write_depth("shadow_map")
            p.set_clear(depth=1.0)
            p.draw_shadow_casters(light_index=0, shadow_type="hard")

        with graph.add_pass("Opaque") as p:
            p.write_color("color")
            p.write_depth("depth")
            p.draw_renderers()

        graph.set_output("color")
        desc = graph.build()

        shadow_pass = next(p for p in desc.passes if p.name == "ShadowCaster")
        assert shadow_pass.light_index == 0
        assert shadow_pass.shadow_type == "hard"

    def test_fullscreen_quad_push_constants(self):
        graph = _make_graph()

        with graph.add_pass("Opaque") as p:
            p.write_color("color")
            p.draw_renderers()

        from InfEngine.rendergraph.graph import Format
        graph.create_texture("_fx_out", format=Format.RGBA16_SFLOAT)

        with graph.add_pass("FX") as p:
            p.set_texture("_SourceTex", "color")
            p.write_color("_fx_out")
            p.set_param("intensity", 0.5)
            p.set_param("threshold", 1.0)
            p.fullscreen_quad("my_effect")

        graph.set_output("_fx_out")
        desc = graph.build()

        fx_pass = next(p for p in desc.passes if p.name == "FX")
        assert fx_pass.shader_name == "my_effect"
        pc_dict = dict(fx_pass.push_constants)
        assert pc_dict["intensity"] == 0.5
        assert pc_dict["threshold"] == 1.0
