from types import SimpleNamespace

import InfEngine.core.texture as texture_module
from InfEngine.core.texture import Texture


class _FakeNativeTexture:
    def __init__(self, width=4, height=4, channels=4, name="fake", source_path=""):
        self.width = width
        self.height = height
        self.channels = channels
        self.name = name
        self.source_path = source_path


def test_texture_load_prefers_load_from_file(monkeypatch):
    calls = []

    def _load_from_file(path, name=""):
        calls.append((path, name))
        return _FakeNativeTexture(source_path=path)

    fake_loader = SimpleNamespace(load_from_file=_load_from_file)
    monkeypatch.setattr(texture_module, "TextureLoader", fake_loader)

    tex = Texture.load("demo.png")

    assert tex is not None
    assert calls == [("demo.png", "")]
    assert tex.source_path == "demo.png"


def test_texture_from_memory_uses_current_binding_signature(monkeypatch):
    calls = []

    def _load_from_memory(data, name=""):
        calls.append((data, name))
        return _FakeNativeTexture(name=name)

    fake_loader = SimpleNamespace(load_from_memory=_load_from_memory)
    monkeypatch.setattr(texture_module, "TextureLoader", fake_loader)

    tex = Texture.from_memory(b"abc", 1, 1, 4, "memory_tex")

    assert tex is not None
    assert calls == [(b"abc", "memory_tex")]
    assert tex.name == "memory_tex"
