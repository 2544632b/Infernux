# execute_in_edit_mode

<div class="class-info">
function in <b>InfEngine.components</b>
</div>

```python
execute_in_edit_mode() → Union[Type, Callable]
```

## Description

Allow a component's ``update()`` to run in edit mode.

Example::

    @execute_in_edit_mode
    class PreviewComponent(InfComponent): ...

<!-- USER CONTENT START --> description

Allows a component's lifecycle methods (`update`, `start`, etc.) to run in the editor outside of Play Mode. This is useful for editor tools, live previews, and components that need to react to Inspector changes in real time.

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.components import execute_in_edit_mode

@execute_in_edit_mode
class LookAtTarget(InfComponent):
    """Continuously faces the target, even in Edit Mode."""
    def update(self):
        target = self.game_object.find("Target")
        if target:
            self.transform.look_at(target.transform.position)
```

<!-- USER CONTENT END -->
