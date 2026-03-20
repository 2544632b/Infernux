# vector2

<div class="class-info">
类位于 <b>InfEngine.math</b>
</div>

## 描述

二维向量，包含 x 和 y 分量。

<!-- USER CONTENT START --> description

vector2 表示具有 `x` 和 `y` 分量的二维向量，在引擎中用于二维位置、方向、UV 坐标和屏幕空间计算。

支持标准算术运算——对向量进行加、减、乘、除运算或按标量缩放。工具方法提供常用操作：`magnitude()` 和 `sqr_magnitude()` 计算长度，`normalize()` 转换为单位向量，`dot()` 计算点积用于投影，`distance()` 计算间距，`lerp()` 进行插值，`angle()` 测量方向之间的旋转角度。

静态常量如 `vector2.zero`、`vector2.one`、`vector2.up` 和 `vector2.right` 提供对常用值的快速访问，无需每次构造新实例。

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| zero | `Vector2` | Vector2(0, 0)。 *(只读)* |
| one | `Vector2` | Vector2(1, 1)。 *(只读)* |
| up | `Vector2` | Vector2(0, 1)。 *(只读)* |
| down | `Vector2` | Vector2(0, -1)。 *(只读)* |
| left | `Vector2` | Vector2(-1, 0)。 *(只读)* |
| right | `Vector2` | Vector2(1, 0)。 *(只读)* |
| positive_infinity | `Vector2` | Shorthand for writing vector2(inf, inf). *(只读)* |
| negative_infinity | `Vector2` | Shorthand for writing vector2(-inf, -inf). *(只读)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `static vector2.angle(a: Vector2, b: Vector2) → float` | 计算两个向量之间的角度。 |
| `static vector2.clamp_magnitude(v: Vector2, max_length: float) → Vector2` | Return a copy of the vector with its magnitude clamped. |
| `static vector2.cross(a: Vector2, b: Vector2) → float` | Return the 2D cross product (z-component of 3D cross). |
| `static vector2.distance(a: Vector2, b: Vector2) → float` | 计算两点之间的距离。 |
| `static vector2.dot(a: Vector2, b: Vector2) → float` | 计算两个向量的点积。 |
| `static vector2.lerp(a: Vector2, b: Vector2, t: float) → Vector2` | 在两个向量之间线性插值。 |
| `static vector2.lerp_unclamped(a: Vector2, b: Vector2, t: float) → Vector2` | Linearly interpolate between two vectors without clamping t. |
| `static vector2.max(a: Vector2, b: Vector2) → Vector2` | Return a vector made from the largest components of two vectors. |
| `static vector2.min(a: Vector2, b: Vector2) → Vector2` | Return a vector made from the smallest components of two vectors. |
| `static vector2.move_towards(current: Vector2, target: Vector2, max_delta: float) → Vector2` | Move current towards target by at most max_delta. |
| `static vector2.normalize(v: Vector2) → Vector2` | 将此向量单位化。 |
| `static vector2.perpendicular(v: Vector2) → Vector2` | Return the 2D vector perpendicular to this vector. |
| `static vector2.reflect(direction: Vector2, normal: Vector2) → Vector2` | Reflect a vector off the surface defined by a normal. |
| `static vector2.scale(a: Vector2, b: Vector2) → Vector2` | Multiply two vectors component-wise. |
| `static vector2.signed_angle(a: Vector2, b: Vector2) → float` | Return the signed angle in degrees between two vectors. |
| `static vector2.smooth_damp(current: Vector2, target: Vector2, current_velocity: Vector2, smooth_time: float, max_speed: float, delta_time: float) → Vector2` | Gradually change a vector towards a desired goal over time. |
| `static vector2.magnitude(v: Vector2) → float` | 向量的长度。 |
| `static vector2.sqr_magnitude(v: Vector2) → float` | 向量长度的平方。 |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine.math import vector2

# 构造向量
pos = vector2(3.0, 4.0)
target = vector2(10.0, 0.0)

# 算术运算
offset = vector2(target.x - pos.x, target.y - pos.y)
scaled = vector2(offset.x * 0.5, offset.y * 0.5)

# 长度与距离
length = vector2.magnitude(pos)           # 5.0
dist = vector2.distance(pos, target)

# 归一化为单位方向
direction = vector2.normalize(offset)

# 点积与角度
dot = vector2.dot(pos, target)
angle = vector2.angle(pos, target)

# 两点之间平滑插值
mid = vector2.lerp(pos, target, 0.5)
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [vector3 三维向量](vector3.md)
- [vector4 四维向量](vector4.md)
- [Transform](Transform.md)

<!-- USER CONTENT END -->
