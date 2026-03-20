from __future__ import annotations

from enum import IntEnum

import pytest

from InfEngine.components.builtin_component import BuiltinComponent, CppProperty
from InfEngine.components.serialized_field import FieldType


class DemoEnum(IntEnum):
    A = 1
    B = 2


class DemoCpp:
    def __init__(self):
        self.mode = 2
        self.raw = 11
        self.locked = 5


class DemoBuiltin(BuiltinComponent):
    _cpp_type_name = "DemoBuiltin"

    mode = CppProperty("mode", FieldType.ENUM, default=DemoEnum.A, enum_type=DemoEnum)
    raw = CppProperty("raw", FieldType.INT, default=7)
    locked = CppProperty("locked", FieldType.INT, default=3, readonly=True)


class LazyEnumBuiltin(BuiltinComponent):
    _cpp_type_name = "LazyEnumBuiltin"

    mode = CppProperty("mode", FieldType.ENUM, default=DemoEnum.A, enum_type="DemoEnum")


def test_cpp_property_returns_defaults_without_cpp():
    demo = DemoBuiltin()
    assert demo.mode is DemoEnum.A
    assert demo.raw == 7


def test_cpp_property_casts_enum_and_sets_raw_values():
    demo = DemoBuiltin()
    cpp = DemoCpp()
    demo._cpp_component = cpp

    assert demo.mode is DemoEnum.B
    assert demo.raw == 11

    demo.mode = DemoEnum.A
    demo.raw = 42

    assert cpp.mode == 1
    assert cpp.raw == 42


def test_cpp_property_rejects_readonly_set():
    demo = DemoBuiltin()
    demo._cpp_component = DemoCpp()

    with pytest.raises(AttributeError):
        demo.locked = 10


def test_cpp_property_can_resolve_lazy_enum_type(fake_infengine_lib):
    fake_module, _ = fake_infengine_lib
    fake_module.DemoEnum = DemoEnum

    demo = LazyEnumBuiltin()
    demo._cpp_component = DemoCpp()
    assert demo.mode is DemoEnum.B