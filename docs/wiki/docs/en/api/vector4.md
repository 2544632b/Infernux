# vector4

<div class="class-info">
class in <b>InfEngine.math</b>
</div>

## Description

A representation of 4D vectors.

<!-- USER CONTENT START --> description

vector4 represents a four-component vector. Common uses include RGBA colors (red, green, blue, alpha), homogeneous 3D coordinates, and passing multi-component values to shaders.

Like vector2 and vector3, all methods are static and operate on `vec4f` values. Arithmetic operators work component-wise, and utility methods such as `lerp()`, `dot()`, and `normalize()` behave identically to their lower-dimension counterparts.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| zero | `vec4f` | Shorthand for writing vector4(0, 0, 0, 0). *(read-only)* |
| one | `vec4f` | Shorthand for writing vector4(1, 1, 1, 1). *(read-only)* |
| positive_infinity | `vec4f` | A vector with all components set to positive infinity. *(read-only)* |
| negative_infinity | `vec4f` | A vector with all components set to negative infinity. *(read-only)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `static vector4.distance(a: vec4f, b: vec4f) → float` | Return the distance between two points. |
| `static vector4.dot(a: vec4f, b: vec4f) → float` | Return the dot product of two vectors. |
| `static vector4.lerp(a: vec4f, b: vec4f, t: float) → vec4f` | Linearly interpolate between two vectors. |
| `static vector4.lerp_unclamped(a: vec4f, b: vec4f, t: float) → vec4f` | Linearly interpolate between two vectors without clamping t. |
| `static vector4.max(a: vec4f, b: vec4f) → vec4f` | Return a vector made from the largest components of two vectors. |
| `static vector4.min(a: vec4f, b: vec4f) → vec4f` | Return a vector made from the smallest components of two vectors. |
| `static vector4.move_towards(current: vec4f, target: vec4f, max_delta: float) → vec4f` | Move current towards target by at most max_delta. |
| `static vector4.normalize(v: vec4f) → vec4f` | Return the vector with a magnitude of 1. |
| `static vector4.project(a: vec4f, b: vec4f) → vec4f` | Project vector a onto vector b. |
| `static vector4.scale(a: vec4f, b: vec4f) → vec4f` | Multiply two vectors component-wise. |
| `static vector4.smooth_damp(current: vec4f, target: vec4f, current_velocity: vec4f, smooth_time: float, max_speed: float, delta_time: float) → vec4f` | Gradually change a vector towards a desired goal over time. |
| `static vector4.magnitude(v: vec4f) → float` | Return the length of the vector. |
| `static vector4.sqr_magnitude(v: vec4f) → float` | Return the squared length of the vector. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine.math import vector4

# RGBA colors
red   = vector4(1, 0, 0, 1)
green = vector4(0, 1, 0, 1)

# Lerp between colors for a fade effect
half = vector4.lerp(red, green, 0.5)   # (0.5, 0.5, 0, 1)

# Magnitude and normalization
v = vector4(1, 2, 3, 4)
length = vector4.magnitude(v)
unit   = vector4.normalize(v)

# Component-wise min / max
a = vector4(3, 1, 4, 2)
b = vector4(1, 5, 2, 6)
lo = vector4.min(a, b)   # (1, 1, 2, 2)
hi = vector4.max(a, b)   # (3, 5, 4, 6)
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [vector2](vector2.md) — 2D vector operations
- [vector3](vector3.md) — 3D vector operations
- [Material](Material.md) — uses vector4 for shader parameters

<!-- USER CONTENT END -->
