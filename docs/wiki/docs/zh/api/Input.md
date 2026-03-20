# Input

<div class="class-info">
类位于 <b>InfEngine.input</b>
</div>

## 描述

用于读取键盘、鼠标和触摸输入的接口。

<!-- USER CONTENT START --> description

Input 提供每帧读取玩家输入的静态接口。支持键盘按键、鼠标按钮、滚轮和虚拟轴。

使用 `get_key()` 进行持续按键检测（例如持续按住时移动），`get_key_down()` 进行单帧按下检测（例如跳跃），`get_key_up()` 进行释放检测。鼠标状态通过 `get_mouse_button()` 及其 `_down` / `_up` 变体查询。

虚拟轴 `"Horizontal"` 和 `"Vertical"` 默认映射到 WASD / 方向键。`get_axis()` 返回平滑后的值（−1 到 1），`get_axis_raw()` 返回未平滑的原始值。

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| mouse_position | `Tuple[float, float]` | 当前鼠标在屏幕坐标中的位置。 *(只读)* |
| game_mouse_position | `Tuple[float, float]` | 当前鼠标在游戏视口坐标中的位置。 *(只读)* |
| mouse_scroll_delta | `Tuple[float, float]` | 当前帧的鼠标滚轮增量。 *(只读)* |
| input_string | `str` | 当前帧中用户输入的字符。 *(只读)* |
| any_key | `bool` | 当任意键或鼠标按钮被按住时返回 True。 *(只读)* |
| any_key_down | `bool` | 当任意键或鼠标按钮首次按下时返回 True。 *(只读)* |
| touch_count | `int` | 当前活动的触摸数量。 *(只读)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `static Input.set_game_focused(focused: bool) → None` | 设置游戏视口是否获得输入焦点。 |
| `static Input.set_game_viewport_origin(x: float, y: float) → None` | 设置游戏视口原点的屏幕坐标。 |
| `static Input.is_game_focused() → bool` | 游戏视口是否获得输入焦点。 |
| `static Input.get_key(key: Union[str, int]) → bool` | 当用户按住指定按键时返回 True。 |
| `static Input.get_key_down(key: Union[str, int]) → bool` | 当用户按下指定按键的那一帧返回 True。 |
| `static Input.get_key_up(key: Union[str, int]) → bool` | 当用户松开指定按键的那一帧返回 True。 |
| `static Input.get_mouse_button(button: int) → bool` | 当鼠标按钮被按住时返回 True。 |
| `static Input.get_mouse_button_down(button: int) → bool` | 当鼠标按钮按下的那一帧返回 True。 |
| `static Input.get_mouse_button_up(button: int) → bool` | 当鼠标按钮松开的那一帧返回 True。 |
| `static Input.get_mouse_position() → Tuple[float, float]` | 获取当前鼠标在屏幕坐标中的位置。 |
| `static Input.get_mouse_scroll_delta() → Tuple[float, float]` | 获取当前帧的鼠标滚轮增量。 |
| `static Input.get_axis(axis_name: str) → float` | 返回经过平滑处理的虚拟轴的值。 |
| `static Input.get_axis_raw(axis_name: str) → float` | 返回未经平滑处理的虚拟轴原始值。 |
| `static Input.get_input_string() → str` | 获取当前帧中用户输入的字符。 |
| `static Input.reset_input_axes() → None` | 将所有输入轴重置为零。 |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.input import Input, KeyCode
from InfEngine.math import vector3

class PlayerController(InfComponent):
    speed: float = 5.0
    jump_force: float = 8.0

    def update(self):
        # 通过虚拟轴移动（WASD / 方向键）
        h = Input.get_axis("Horizontal")
        v = Input.get_axis("Vertical")
        move = vector3(h, 0, v) * self.speed * self.time.delta_time
        self.transform.translate(move)

        # 按空格跳跃
        if Input.get_key_down(KeyCode.SPACE):
            Debug.log("跳跃！")

        # 按住 Shift 加速
        if Input.get_key(KeyCode.LEFT_SHIFT):
            self.transform.translate(move)  # 双倍速度

        # 鼠标左键射击
        if Input.get_mouse_button_down(0):
            Debug.log("开火！")
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [KeyCode](KeyCode.md) — 与 Input 方法一起使用的按键常量
- [InfComponent](InfComponent.md) — 读取输入的生命周期方法

<!-- USER CONTENT END -->
