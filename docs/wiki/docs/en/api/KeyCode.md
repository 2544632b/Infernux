# KeyCode

<div class="class-info">
class in <b>InfEngine.input</b>
</div>

## Description

Key code constants for keyboard input.

<!-- USER CONTENT START --> description

KeyCode defines integer constants for every keyboard key and mouse button. Pass these values to [Input](Input.md) methods such as `Input.get_key()`, `Input.get_key_down()`, and `Input.get_key_up()` to query specific key states.

Common groups include letter keys (`A`–`Z`), digit keys (`ALPHA0`–`ALPHA9`), function keys (`F1`–`F12`), arrow keys, modifier keys (Shift, Control, Alt), and numpad keys.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| NONE | `int` |  *(read-only)* |
| BACKSPACE | `int` |  *(read-only)* |
| TAB | `int` |  *(read-only)* |
| RETURN | `int` |  *(read-only)* |
| ESCAPE | `int` |  *(read-only)* |
| SPACE | `int` |  *(read-only)* |
| DELETE | `int` |  *(read-only)* |
| ALPHA0 | `int` |  *(read-only)* |
| ALPHA1 | `int` |  *(read-only)* |
| ALPHA2 | `int` |  *(read-only)* |
| ALPHA3 | `int` |  *(read-only)* |
| ALPHA4 | `int` |  *(read-only)* |
| ALPHA5 | `int` |  *(read-only)* |
| ALPHA6 | `int` |  *(read-only)* |
| ALPHA7 | `int` |  *(read-only)* |
| ALPHA8 | `int` |  *(read-only)* |
| ALPHA9 | `int` |  *(read-only)* |
| A | `int` |  *(read-only)* |
| B | `int` |  *(read-only)* |
| C | `int` |  *(read-only)* |
| D | `int` |  *(read-only)* |
| E | `int` |  *(read-only)* |
| F | `int` |  *(read-only)* |
| G | `int` |  *(read-only)* |
| H | `int` |  *(read-only)* |
| I | `int` |  *(read-only)* |
| J | `int` |  *(read-only)* |
| K | `int` |  *(read-only)* |
| L | `int` |  *(read-only)* |
| M | `int` |  *(read-only)* |
| N | `int` |  *(read-only)* |
| O | `int` |  *(read-only)* |
| P | `int` |  *(read-only)* |
| Q | `int` |  *(read-only)* |
| R | `int` |  *(read-only)* |
| S | `int` |  *(read-only)* |
| T | `int` |  *(read-only)* |
| U | `int` |  *(read-only)* |
| V | `int` |  *(read-only)* |
| W | `int` |  *(read-only)* |
| X | `int` |  *(read-only)* |
| Y | `int` |  *(read-only)* |
| Z | `int` |  *(read-only)* |
| F1 | `int` |  *(read-only)* |
| F2 | `int` |  *(read-only)* |
| F3 | `int` |  *(read-only)* |
| F4 | `int` |  *(read-only)* |
| F5 | `int` |  *(read-only)* |
| F6 | `int` |  *(read-only)* |
| F7 | `int` |  *(read-only)* |
| F8 | `int` |  *(read-only)* |
| F9 | `int` |  *(read-only)* |
| F10 | `int` |  *(read-only)* |
| F11 | `int` |  *(read-only)* |
| F12 | `int` |  *(read-only)* |
| UP_ARROW | `int` |  *(read-only)* |
| DOWN_ARROW | `int` |  *(read-only)* |
| LEFT_ARROW | `int` |  *(read-only)* |
| RIGHT_ARROW | `int` |  *(read-only)* |
| LEFT_SHIFT | `int` |  *(read-only)* |
| RIGHT_SHIFT | `int` |  *(read-only)* |
| LEFT_CONTROL | `int` |  *(read-only)* |
| RIGHT_CONTROL | `int` |  *(read-only)* |
| LEFT_ALT | `int` |  *(read-only)* |
| RIGHT_ALT | `int` |  *(read-only)* |
| LEFT_COMMAND | `int` |  *(read-only)* |
| RIGHT_COMMAND | `int` |  *(read-only)* |
| KEYPAD0 | `int` |  *(read-only)* |
| KEYPAD1 | `int` |  *(read-only)* |
| KEYPAD2 | `int` |  *(read-only)* |
| KEYPAD3 | `int` |  *(read-only)* |
| KEYPAD4 | `int` |  *(read-only)* |
| KEYPAD5 | `int` |  *(read-only)* |
| KEYPAD6 | `int` |  *(read-only)* |
| KEYPAD7 | `int` |  *(read-only)* |
| KEYPAD8 | `int` |  *(read-only)* |
| KEYPAD9 | `int` |  *(read-only)* |
| KEYPAD_PERIOD | `int` |  *(read-only)* |
| KEYPAD_DIVIDE | `int` |  *(read-only)* |
| KEYPAD_MULTIPLY | `int` |  *(read-only)* |
| KEYPAD_MINUS | `int` |  *(read-only)* |
| KEYPAD_PLUS | `int` |  *(read-only)* |
| KEYPAD_ENTER | `int` |  *(read-only)* |
| MINUS | `int` |  *(read-only)* |
| EQUALS | `int` |  *(read-only)* |
| LEFT_BRACKET | `int` |  *(read-only)* |
| RIGHT_BRACKET | `int` |  *(read-only)* |
| BACKSLASH | `int` |  *(read-only)* |
| SEMICOLON | `int` |  *(read-only)* |
| QUOTE | `int` |  *(read-only)* |
| BACKQUOTE | `int` |  *(read-only)* |
| COMMA | `int` |  *(read-only)* |
| PERIOD | `int` |  *(read-only)* |
| SLASH | `int` |  *(read-only)* |
| CAPS_LOCK | `int` |  *(read-only)* |
| INSERT | `int` |  *(read-only)* |
| HOME | `int` |  *(read-only)* |
| END | `int` |  *(read-only)* |
| PAGE_UP | `int` |  *(read-only)* |
| PAGE_DOWN | `int` |  *(read-only)* |
| PRINT_SCREEN | `int` |  *(read-only)* |
| SCROLL_LOCK | `int` |  *(read-only)* |
| PAUSE | `int` |  *(read-only)* |
| NUM_LOCK | `int` |  *(read-only)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.input import Input, KeyCode
from InfEngine.math import vector3

class KeyCodeDemo(InfComponent):
    def update(self):
        # WASD movement
        move = vector3.zero
        if Input.get_key(KeyCode.W):
            move += vector3.forward
        if Input.get_key(KeyCode.S):
            move -= vector3.forward
        if Input.get_key(KeyCode.A):
            move -= vector3.right
        if Input.get_key(KeyCode.D):
            move += vector3.right
        self.transform.translate(move * 5.0 * self.time.delta_time)

        # Action keys
        if Input.get_key_down(KeyCode.SPACE):
            Debug.log("Jump")
        if Input.get_key_down(KeyCode.ESCAPE):
            Debug.log("Pause")

        # Number keys for item selection
        for i in range(10):
            code = getattr(KeyCode, f"ALPHA{i}")
            if Input.get_key_down(code):
                Debug.log(f"Selected slot {i}")
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Input](Input.md) — reads key states using KeyCode values

<!-- USER CONTENT END -->
