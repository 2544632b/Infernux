# disallow_multiple

<div class="class-info">
function in <b>InfEngine.components</b>
</div>

```python
disallow_multiple() → Union[Type, Callable]
```

## Description

Prevent multiple instances of this component on a GameObject.

Usable with or without parentheses::

    @disallow_multiple
    class MySingleton(InfComponent): ...

    @disallow_multiple()
    class MySingleton(InfComponent): ...

<!-- USER CONTENT START --> description

Prevents more than one instance of this component type from being attached to the same GameObject. The engine will refuse to add a duplicate and log a warning.

Equivalent to Unity's `[DisallowMultipleComponent]` attribute. Can be used with or without parentheses.

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.components import disallow_multiple

@disallow_multiple
class GameManager(InfComponent):
    """Only one GameManager per GameObject."""
    def start(self):
        Debug.log("GameManager initialized")
```

<!-- USER CONTENT END -->
