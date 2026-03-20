# vector4

<div class="class-info">
类位于 <b>InfEngine.math</b>
</div>

## 描述

四维向量，包含 x、y、z 和 w 分量。

<!-- USER CONTENT START --> description

vector4 表示四分量向量。常见用途包括 RGBA 颜色（红、绿、蓝、透明度）、齐次 3D 坐标以及向着色器传递多分量值。

与 vector2 和 vector3 一样，所有方法都是静态的，操作 `vec4f` 值。算术运算符按分量运算，`lerp()`、`dot()` 和 `normalize()` 等工具方法与低维版本行为一致。

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| zero | `vec4f` | Vector4(0, 0, 0, 0)。 *(只读)* |
| one | `vec4f` | Vector4(1, 1, 1, 1)。 *(只读)* |
| positive_infinity | `vec4f` | A vector with all components set to positive infinity. *(只读)* |
| negative_infinity | `vec4f` | A vector with all components set to negative infinity. *(只读)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `static vector4.distance(a: vec4f, b: vec4f) → float` | 计算两点之间的距离。 |
| `static vector4.dot(a: vec4f, b: vec4f) → float` | 计算两个向量的点积。 |
| `static vector4.lerp(a: vec4f, b: vec4f, t: float) → vec4f` | 在两个向量之间线性插值。 |
| `static vector4.lerp_unclamped(a: vec4f, b: vec4f, t: float) → vec4f` | Linearly interpolate between two vectors without clamping t. |
| `static vector4.max(a: vec4f, b: vec4f) → vec4f` | Return a vector made from the largest components of two vectors. |
| `static vector4.min(a: vec4f, b: vec4f) → vec4f` | Return a vector made from the smallest components of two vectors. |
| `static vector4.move_towards(current: vec4f, target: vec4f, max_delta: float) → vec4f` | Move current towards target by at most max_delta. |
| `static vector4.normalize(v: vec4f) → vec4f` | 将此向量单位化。 |
| `static vector4.project(a: vec4f, b: vec4f) → vec4f` | Project vector a onto vector b. |
| `static vector4.scale(a: vec4f, b: vec4f) → vec4f` | Multiply two vectors component-wise. |
| `static vector4.smooth_damp(current: vec4f, target: vec4f, current_velocity: vec4f, smooth_time: float, max_speed: float, delta_time: float) → vec4f` | Gradually change a vector towards a desired goal over time. |
| `static vector4.magnitude(v: vec4f) → float` | 向量的长度。 |
| `static vector4.sqr_magnitude(v: vec4f) → float` | 向量长度的平方。 |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine.math import vector4

# RGBA 颜色
red   = vector4(1, 0, 0, 1)
green = vector4(0, 1, 0, 1)

# 在颜色之间插值实现渐变效果
half = vector4.lerp(red, green, 0.5)   # (0.5, 0.5, 0, 1)

# 长度与归一化
v = vector4(1, 2, 3, 4)
length = vector4.magnitude(v)
unit   = vector4.normalize(v)

# 按分量取最小值 / 最大值
a = vector4(3, 1, 4, 2)
b = vector4(1, 5, 2, 6)
lo = vector4.min(a, b)   # (1, 1, 2, 2)
hi = vector4.max(a, b)   # (3, 5, 4, 6)
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [vector2](vector2.md) — 二维向量运算
- [vector3](vector3.md) — 三维向量运算
- [Material](Material.md) — 使用 vector4 传递着色器参数

<!-- USER CONTENT END -->
