# add_component_menu

<div class="class-info">
函数位于 <b>InfEngine.components</b>
</div>

```python
add_component_menu(path: str) → Callable
```

## 描述

Specify where this component appears in the Add Component menu.

Args:
    path: Menu path like ``"Physics/Character Controller"``.

<!-- USER CONTENT START --> description

指定此组件在编辑器的 **添加组件** 菜单中的显示路径。使用斜杠创建嵌套类别（例如 `"Gameplay/AI/Patrol"`）。

未使用此装饰器时，自定义组件会显示在菜单的顶层。

<!-- USER CONTENT END -->

## 参数

| 名称 | 类型 | 描述 |
|------|------|------|
| path | `str` |  |

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.components import add_component_menu

@add_component_menu("Gameplay/Character/PlayerController")
class PlayerController(InfComponent):
    """在“添加组件”菜单中显示在 Gameplay > Character 下。"""
    def update(self):
        pass
```

<!-- USER CONTENT END -->
