# serialized_field

<div class="class-info">
function in <b>InfEngine.components</b>
</div>

```python
serialized_field(default: Any = ..., field_type: Optional[FieldType] = ..., element_type: Optional[FieldType] = ..., element_class: Optional[Type] = ..., serializable_class: Optional[Type] = ..., component_type: Optional[str] = ..., range: Optional[Tuple[float, float]] = ..., tooltip: str = ..., readonly: bool = ..., header: str = ..., space: float = ..., group: str = ..., info_text: str = ..., multiline: bool = ..., slider: bool = ..., drag_speed: Optional[float] = ..., required_component: Optional[str] = ..., visible_when: Optional[Callable] = ..., hdr: bool = ...) → Any
```

## Description

Mark a field as serialized and inspector-visible.

Args:
    default: Default value for the field.
    field_type: Explicit field type (auto-detected if not provided).
    element_type: For LIST fields, the element FieldType.
    element_class: For LIST fields, the SerializableObject subclass for elements.
    serializable_class: For SERIALIZABLE_OBJECT fields, the concrete class.
    component_type: For COMPONENT fields, the target component type name.
    range: ``(min, max)`` tuple for numeric sliders / bounded drag.
    tooltip: Hover text shown in inspector.
    readonly: If ``True``, field is read-only in inspector.
    header: Group header text shown above this field.
    space: Vertical spacing before this field in inspector.
    group: Collapsible group name.
    info_text: Non-editable description line (dimmed) below the field.
    multiline: Use multiline text input for STRING fields.
    slider: Widget style when range is set (True = slider, False = drag).
    drag_speed: Override default drag speed for numeric fields.
    required_component: For GAME_OBJECT fields only.
    visible_when: ``fn(component) -> bool``; hides field when False.
    hdr: For COLOR fields only.  Allow HDR values (> 1.0).

Example::

    class MyComponent(InfComponent):
        speed: float = serialized_field(default=5.0, range=(0, 100))

<!-- USER CONTENT START --> description

`serialized_field` marks a class attribute as serialized and visible in the Inspector. It is the primary way to expose component data for editing in the InfEngine editor and for scene/prefab serialization.

Supported field types include numbers (`int`, `float`), strings, booleans, vectors, colors, enums, GameObjects, Components, and lists. Each field can be customized with tooltips, ranges, headers, groups, and visibility callbacks.

<!-- USER CONTENT END -->

## Parameters

| Name | Type | Description |
|------|------|------|
| default | `Any` |  (default: `...`) |
| field_type | `Optional[FieldType]` |  (default: `...`) |
| element_type | `Optional[FieldType]` |  (default: `...`) |
| element_class | `Optional[Type]` |  (default: `...`) |
| serializable_class | `Optional[Type]` |  (default: `...`) |
| component_type | `Optional[str]` |  (default: `...`) |
| range | `Optional[Tuple[float, float]]` |  (default: `...`) |
| tooltip | `str` |  (default: `...`) |
| readonly | `bool` |  (default: `...`) |
| header | `str` |  (default: `...`) |
| space | `float` |  (default: `...`) |
| group | `str` |  (default: `...`) |
| info_text | `str` |  (default: `...`) |
| multiline | `bool` |  (default: `...`) |
| slider | `bool` |  (default: `...`) |
| drag_speed | `Optional[float]` |  (default: `...`) |
| required_component | `Optional[str]` |  (default: `...`) |
| visible_when | `Optional[Callable]` |  (default: `...`) |
| hdr | `bool` |  (default: `...`) |

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.components import serialized_field

class Enemy(InfComponent):
    # Basic numeric fields with Inspector hints
    health: float = serialized_field(default=100.0, range=(0, 500),
                                      tooltip="Maximum hit points")
    speed: float = serialized_field(default=3.0, range=(0, 20), slider=True)

    # String with header and multiline
    description: str = serialized_field(default="", header="Info",
                                         multiline=True)

    # Read-only status shown in Inspector
    is_alive: bool = serialized_field(default=True, readonly=True)

    # Grouped fields with conditional visibility
    use_patrol: bool = serialized_field(default=False, group="AI")
    patrol_radius: float = serialized_field(
        default=10.0, group="AI",
        visible_when=lambda self: self.use_patrol
    )
```

<!-- USER CONTENT END -->
