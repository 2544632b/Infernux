# Input

<div class="class-info">
class in <b>InfEngine.input</b>
</div>

## Description

Interface for reading input from keyboard, mouse, and touch.

<!-- USER CONTENT START --> description

Input provides a static interface for reading player input each frame. It supports keyboard keys, mouse buttons, scroll wheel, and virtual axes.

Use `get_key()` for continuous held-key checks (e.g., moving while a key is held), `get_key_down()` for single-frame press detection (e.g., jumping), and `get_key_up()` for release detection. Mouse state is queried with `get_mouse_button()` and its `_down` / `_up` variants.

Virtual axes `"Horizontal"` and `"Vertical"` map to WASD / arrow keys by default. `get_axis()` returns a smoothed value (−1 to 1), while `get_axis_raw()` returns the unsmoothed value.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| mouse_position | `Tuple[float, float]` | The current mouse position in screen coordinates. *(read-only)* |
| game_mouse_position | `Tuple[float, float]` | The current mouse position in game viewport coordinates. *(read-only)* |
| mouse_scroll_delta | `Tuple[float, float]` | The mouse scroll delta for the current frame. *(read-only)* |
| input_string | `str` | Characters typed by the user in the current frame. *(read-only)* |
| any_key | `bool` | Returns True while any key or mouse button is held down. *(read-only)* |
| any_key_down | `bool` | Returns True during the frame any key or mouse button is first pressed. *(read-only)* |
| touch_count | `int` | Number of active touch contacts. *(read-only)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `static Input.set_game_focused(focused: bool) → None` | Set whether the game viewport has input focus. |
| `static Input.set_game_viewport_origin(x: float, y: float) → None` | Set the game viewport origin in screen coordinates. |
| `static Input.is_game_focused() → bool` | Returns True if the game viewport has input focus. |
| `static Input.get_key(key: Union[str, int]) → bool` | Returns True while the user holds down the specified key. |
| `static Input.get_key_down(key: Union[str, int]) → bool` | Returns True during the frame the user starts pressing the key. |
| `static Input.get_key_up(key: Union[str, int]) → bool` | Returns True during the frame the user releases the key. |
| `static Input.get_mouse_button(button: int) → bool` | Returns True while the given mouse button is held down. |
| `static Input.get_mouse_button_down(button: int) → bool` | Returns True during the frame the mouse button was pressed. |
| `static Input.get_mouse_button_up(button: int) → bool` | Returns True during the frame the mouse button was released. |
| `static Input.get_mouse_position() → Tuple[float, float]` | Get the current mouse position in screen coordinates. |
| `static Input.get_mouse_scroll_delta() → Tuple[float, float]` | Get the mouse scroll delta for the current frame. |
| `static Input.get_axis(axis_name: str) → float` | Returns the value of the virtual axis identified by axis_name. |
| `static Input.get_axis_raw(axis_name: str) → float` | Returns the raw value of the virtual axis with no smoothing. |
| `static Input.get_input_string() → str` | Get the characters typed by the user in the current frame. |
| `static Input.reset_input_axes() → None` | Reset all input axes to zero. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.input import Input, KeyCode
from InfEngine.math import vector3

class PlayerController(InfComponent):
    speed: float = 5.0
    jump_force: float = 8.0

    def update(self):
        # Movement via virtual axes (WASD / arrow keys)
        h = Input.get_axis("Horizontal")
        v = Input.get_axis("Vertical")
        move = vector3(h, 0, v) * self.speed * self.time.delta_time
        self.transform.translate(move)

        # Jump on Space press
        if Input.get_key_down(KeyCode.SPACE):
            Debug.log("Jump!")

        # Sprint while Shift is held
        if Input.get_key(KeyCode.LEFT_SHIFT):
            self.transform.translate(move)  # double speed

        # Shoot on left mouse button
        if Input.get_mouse_button_down(0):
            Debug.log("Fire!")
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [KeyCode](KeyCode.md) — key constants used with Input methods
- [InfComponent](InfComponent.md) — lifecycle methods where input is read

<!-- USER CONTENT END -->
