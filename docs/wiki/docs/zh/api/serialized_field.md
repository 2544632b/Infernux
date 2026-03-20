# serialized_field

<div class="class-info">
函数位于 <b>InfEngine.components</b>
</div>

```python
serialized_field(default: Any = ..., field_type: Optional[FieldType] = ..., element_type: Optional[FieldType] = ..., element_class: Optional[Type] = ..., serializable_class: Optional[Type] = ..., component_type: Optional[str] = ..., range: Optional[Tuple[float, float]] = ..., tooltip: str = ..., readonly: bool = ..., header: str = ..., space: float = ..., group: str = ..., info_text: str = ..., multiline: bool = ..., slider: bool = ..., drag_speed: Optional[float] = ..., required_component: Optional[str] = ..., visible_when: Optional[Callable] = ..., hdr: bool = ...) → Any
```

## 描述

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

`serialized_field` 将类属性标记为序列化字段并在检查器中可见。它是在 InfEngine 编辑器中暴露组件数据以及场景/预制件序列化的主要方式。

支持的字段类型包括数值（`int`、`float`）、字符串、布尔值、向量、颜色、枚举、GameObject、Component 和列表。每个字段可通过提示信息、范围、标题、分组和可见性回调进行自定义。

<!-- USER CONTENT END -->

## 参数

| 名称 | 类型 | 描述 |
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

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.components import serialized_field

class Enemy(InfComponent):
    # 基本数值字段，带检查器提示
    health: float = serialized_field(default=100.0, range=(0, 500),
                                      tooltip="最大生命值")
    speed: float = serialized_field(default=3.0, range=(0, 20), slider=True)

    # 带标题和多行输入的字符串
    description: str = serialized_field(default="", header="信息",
                                         multiline=True)

    # 检查器中的只读状态
    is_alive: bool = serialized_field(default=True, readonly=True)

    # 分组字段，带条件可见性
    use_patrol: bool = serialized_field(default=False, group="AI")
    patrol_radius: float = serialized_field(
        default=10.0, group="AI",
        visible_when=lambda self: self.use_patrol
    )
```

<!-- USER CONTENT END -->
