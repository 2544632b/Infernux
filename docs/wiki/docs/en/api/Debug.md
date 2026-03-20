# Debug

<div class="class-info">
class in <b>InfEngine.debug</b>
</div>

## Description

Utility class for logging messages to the console.

<!-- USER CONTENT START --> description

Debug provides logging and visual diagnostic utilities. Messages appear in the engine console with severity levels: **Log**, **Warning**, and **Error**.

Use `Debug.log()` for general information, `Debug.log_warning()` for potential issues, and `Debug.log_error()` for errors that need attention. `Debug.log_assert()` can validate conditions during development. Call `Debug.clear_console()` to reset the console output.

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `static Debug.log(message: Any, context: Any = ...) → None` | Log a message to the console. |
| `static Debug.log_warning(message: Any, context: Any = ...) → None` | Log a warning message to the console. |
| `static Debug.log_error(message: Any, context: Any = ..., source_file: str = ..., source_line: int = ...) → None` | Log an error message to the console. |
| `static Debug.log_exception(exception: Exception, context: Any = ...) → None` | Log an exception to the console. |
| `static Debug.log_assert(condition: bool, message: Any = ..., context: Any = ...) → None` | Assert a condition and log if it fails. |
| `static Debug.clear_console() → None` | Clear all messages in the debug console. |
| `static Debug.log_internal(message: Any, context: Any = ...) → None` | Log an internal engine message (hidden from user by default). |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.debug import Debug

class DebugExample(InfComponent):
    def start(self):
        Debug.log("Game started")
        Debug.log_warning("Low memory")
        Debug.log_error("Shader compilation failed")

    def update(self):
        # Assert a condition during development
        Debug.log_assert(self.game_object is not None, "Missing game object")

        # Log once with context
        if self.time.frame_count == 1:
            Debug.log(f"First frame delta: {self.time.delta_time}", self)
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Gizmos](Gizmos.md) — visual debugging in the Scene view
- [InfComponent](InfComponent.md) — component lifecycle

<!-- USER CONTENT END -->
