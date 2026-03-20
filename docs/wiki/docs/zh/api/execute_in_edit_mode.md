# execute_in_edit_mode

<div class="class-info">
函数位于 <b>InfEngine.components</b>
</div>

```python
execute_in_edit_mode() → Union[Type, Callable]
```

## 描述

Allow a component's ``update()`` to run in edit mode.

Example::

    @execute_in_edit_mode
    class PreviewComponent(InfComponent): ...

<!-- USER CONTENT START --> description

允许组件的生命周期方法（`update`、`start` 等）在编辑器的非播放模式下运行。适用于编辑器工具、实时预览以及需要实时响应检查器更改的组件。

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.components import execute_in_edit_mode

@execute_in_edit_mode
class LookAtTarget(InfComponent):
    """持续朝向目标，即使在编辑模式下也生效。"""
    def update(self):
        target = self.game_object.find("Target")
        if target:
            self.transform.look_at(target.transform.position)
```

<!-- USER CONTENT END -->
