# require_component

<div class="class-info">
函数位于 <b>InfEngine.components</b>
</div>

```python
require_component() → Callable
```

## 描述

Declare that a component requires other component types.

Example::

    @require_component(Rigidbody, Collider)
    class PhysicsController(InfComponent): ...

<!-- USER CONTENT START --> description

确保在将此组件附加到 GameObject 时自动添加所需的组件类型。如果所需组件尚不存在，引擎会自动添加。

这可以防止因缺少依赖而导致的运行时错误，等价于 Unity 的 `[RequireComponent]` 特性。

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.components import require_component
from InfEngine.rendering import MeshRenderer

@require_component(MeshRenderer)
class HealthBar(InfComponent):
    """需要 MeshRenderer——如果缺少会自动添加。"""
    def start(self):
        renderer = self.get_component(MeshRenderer)
        renderer.material.set_color("_Color", (0, 1, 0))
```

<!-- USER CONTENT END -->
