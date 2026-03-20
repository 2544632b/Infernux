# require_component

<div class="class-info">
function in <b>InfEngine.components</b>
</div>

```python
require_component() → Callable
```

## Description

Declare that a component requires other component types.

Example::

    @require_component(Rigidbody, Collider)
    class PhysicsController(InfComponent): ...

<!-- USER CONTENT START --> description

Ensures that required component types are automatically added when this component is attached to a GameObject. If the required components are not already present, the engine adds them.

This prevents runtime errors caused by missing dependencies and is equivalent to Unity's `[RequireComponent]` attribute.

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.components import require_component
from InfEngine.rendering import MeshRenderer

@require_component(MeshRenderer)
class HealthBar(InfComponent):
    """Requires a MeshRenderer — one is added automatically if missing."""
    def start(self):
        renderer = self.get_component(MeshRenderer)
        renderer.material.set_color("_Color", (0, 1, 0))
```

<!-- USER CONTENT END -->
