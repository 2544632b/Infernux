# KeyCode

<div class="class-info">
类位于 <b>InfEngine.input</b>
</div>

## 描述

按键代码枚举，用于标识键盘和鼠标按键。

<!-- USER CONTENT START --> description

KeyCode 定义了每个键盘按键和鼠标按钮的整数常量。将这些值传递给 [Input](Input.md) 的 `Input.get_key()`、`Input.get_key_down()` 和 `Input.get_key_up()` 方法来查询特定按键状态。

常用分组包括字母键（`A`–`Z`）、数字键（`ALPHA0`–`ALPHA9`）、功能键（`F1`–`F12`）、方向键、修饰键（Shift、Control、Alt）和小键盘按键。

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| NONE | `int` |  *(只读)* |
| BACKSPACE | `int` |  *(只读)* |
| TAB | `int` |  *(只读)* |
| RETURN | `int` |  *(只读)* |
| ESCAPE | `int` |  *(只读)* |
| SPACE | `int` |  *(只读)* |
| DELETE | `int` |  *(只读)* |
| ALPHA0 | `int` |  *(只读)* |
| ALPHA1 | `int` |  *(只读)* |
| ALPHA2 | `int` |  *(只读)* |
| ALPHA3 | `int` |  *(只读)* |
| ALPHA4 | `int` |  *(只读)* |
| ALPHA5 | `int` |  *(只读)* |
| ALPHA6 | `int` |  *(只读)* |
| ALPHA7 | `int` |  *(只读)* |
| ALPHA8 | `int` |  *(只读)* |
| ALPHA9 | `int` |  *(只读)* |
| A | `int` |  *(只读)* |
| B | `int` |  *(只读)* |
| C | `int` |  *(只读)* |
| D | `int` |  *(只读)* |
| E | `int` |  *(只读)* |
| F | `int` |  *(只读)* |
| G | `int` |  *(只读)* |
| H | `int` |  *(只读)* |
| I | `int` |  *(只读)* |
| J | `int` |  *(只读)* |
| K | `int` |  *(只读)* |
| L | `int` |  *(只读)* |
| M | `int` |  *(只读)* |
| N | `int` |  *(只读)* |
| O | `int` |  *(只读)* |
| P | `int` |  *(只读)* |
| Q | `int` |  *(只读)* |
| R | `int` |  *(只读)* |
| S | `int` |  *(只读)* |
| T | `int` |  *(只读)* |
| U | `int` |  *(只读)* |
| V | `int` |  *(只读)* |
| W | `int` |  *(只读)* |
| X | `int` |  *(只读)* |
| Y | `int` |  *(只读)* |
| Z | `int` |  *(只读)* |
| F1 | `int` |  *(只读)* |
| F2 | `int` |  *(只读)* |
| F3 | `int` |  *(只读)* |
| F4 | `int` |  *(只读)* |
| F5 | `int` |  *(只读)* |
| F6 | `int` |  *(只读)* |
| F7 | `int` |  *(只读)* |
| F8 | `int` |  *(只读)* |
| F9 | `int` |  *(只读)* |
| F10 | `int` |  *(只读)* |
| F11 | `int` |  *(只读)* |
| F12 | `int` |  *(只读)* |
| UP_ARROW | `int` |  *(只读)* |
| DOWN_ARROW | `int` |  *(只读)* |
| LEFT_ARROW | `int` |  *(只读)* |
| RIGHT_ARROW | `int` |  *(只读)* |
| LEFT_SHIFT | `int` |  *(只读)* |
| RIGHT_SHIFT | `int` |  *(只读)* |
| LEFT_CONTROL | `int` |  *(只读)* |
| RIGHT_CONTROL | `int` |  *(只读)* |
| LEFT_ALT | `int` |  *(只读)* |
| RIGHT_ALT | `int` |  *(只读)* |
| LEFT_COMMAND | `int` |  *(只读)* |
| RIGHT_COMMAND | `int` |  *(只读)* |
| KEYPAD0 | `int` |  *(只读)* |
| KEYPAD1 | `int` |  *(只读)* |
| KEYPAD2 | `int` |  *(只读)* |
| KEYPAD3 | `int` |  *(只读)* |
| KEYPAD4 | `int` |  *(只读)* |
| KEYPAD5 | `int` |  *(只读)* |
| KEYPAD6 | `int` |  *(只读)* |
| KEYPAD7 | `int` |  *(只读)* |
| KEYPAD8 | `int` |  *(只读)* |
| KEYPAD9 | `int` |  *(只读)* |
| KEYPAD_PERIOD | `int` |  *(只读)* |
| KEYPAD_DIVIDE | `int` |  *(只读)* |
| KEYPAD_MULTIPLY | `int` |  *(只读)* |
| KEYPAD_MINUS | `int` |  *(只读)* |
| KEYPAD_PLUS | `int` |  *(只读)* |
| KEYPAD_ENTER | `int` |  *(只读)* |
| MINUS | `int` |  *(只读)* |
| EQUALS | `int` |  *(只读)* |
| LEFT_BRACKET | `int` |  *(只读)* |
| RIGHT_BRACKET | `int` |  *(只读)* |
| BACKSLASH | `int` |  *(只读)* |
| SEMICOLON | `int` |  *(只读)* |
| QUOTE | `int` |  *(只读)* |
| BACKQUOTE | `int` |  *(只读)* |
| COMMA | `int` |  *(只读)* |
| PERIOD | `int` |  *(只读)* |
| SLASH | `int` |  *(只读)* |
| CAPS_LOCK | `int` |  *(只读)* |
| INSERT | `int` |  *(只读)* |
| HOME | `int` |  *(只读)* |
| END | `int` |  *(只读)* |
| PAGE_UP | `int` |  *(只读)* |
| PAGE_DOWN | `int` |  *(只读)* |
| PRINT_SCREEN | `int` |  *(只读)* |
| SCROLL_LOCK | `int` |  *(只读)* |
| PAUSE | `int` |  *(只读)* |
| NUM_LOCK | `int` |  *(只读)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.input import Input, KeyCode
from InfEngine.math import vector3

class KeyCodeDemo(InfComponent):
    def update(self):
        # WASD 移动
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

        # 动作按键
        if Input.get_key_down(KeyCode.SPACE):
            Debug.log("跳跃")
        if Input.get_key_down(KeyCode.ESCAPE):
            Debug.log("暂停")

        # 数字键选择物品栏
        for i in range(10):
            code = getattr(KeyCode, f"ALPHA{i}")
            if Input.get_key_down(code):
                Debug.log(f"选择了槽位 {i}")
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Input](Input.md) — 使用 KeyCode 值读取按键状态

<!-- USER CONTENT END -->
