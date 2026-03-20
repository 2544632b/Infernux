from InfEngine.components import InfComponent
from InfEngine.components.serialized_field import get_serialized_fields


class AnnotationDefaultsComponent(InfComponent):
    c: int
    speed: float
    enabled_flag: bool
    label: str


class HiddenAnnotationDefaultsComponent(InfComponent):
    _c: int
    _items: list[int]


def test_annotation_only_primitive_fields_get_default_values():
    comp = AnnotationDefaultsComponent()

    assert comp.c == 0
    assert comp.speed == 0.0
    assert comp.enabled_flag is False
    assert comp.label == ""

    comp.c += 1
    comp.speed += 2.5
    comp.enabled_flag = True
    comp.label = "ok"

    assert comp.c == 1
    assert comp.speed == 2.5
    assert comp.enabled_flag is True
    assert comp.label == "ok"


def test_private_annotation_only_fields_are_hidden_but_initialized():
    comp = HiddenAnnotationDefaultsComponent()

    assert comp._c == 0
    assert comp._items == []

    comp._c += 1
    comp._items.append("x")

    assert comp._c == 1
    assert comp._items == ["x"]
    assert "_c" not in get_serialized_fields(HiddenAnnotationDefaultsComponent)
    assert "_items" not in get_serialized_fields(HiddenAnnotationDefaultsComponent)
