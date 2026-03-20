# vector3

<div class="class-info">
class in <b>InfEngine.math</b>
</div>

## Description

A representation of 3D vectors and points.

<!-- USER CONTENT START --> description

vector3 is the most frequently used type in InfEngine. It represents positions, directions, velocities, and scales in three-dimensional space. Every [Transform](Transform.md) stores its `position`, `rotation`, and `local_scale` as vector3 values, and physics, rendering, and animation systems all operate on them.

Arithmetic operators (`+`, `-`, `*`, `/`) work component-wise. Use `dot()` to measure alignment between two directions, `cross()` to compute perpendicular vectors (e.g., surface normals), and `project()` / `project_on_plane()` for projection.

Static direction constants — `forward` (0, 0, 1), `up` (0, 1, 0), `right` (1, 0, 0) — follow InfEngine's left-hand coordinate system conventions.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| zero | `Vector3` | Shorthand for writing vector3(0, 0, 0). *(read-only)* |
| one | `Vector3` | Shorthand for writing vector3(1, 1, 1). *(read-only)* |
| up | `Vector3` | Shorthand for writing vector3(0, 1, 0). *(read-only)* |
| down | `Vector3` | Shorthand for writing vector3(0, -1, 0). *(read-only)* |
| left | `Vector3` | Shorthand for writing vector3(-1, 0, 0). *(read-only)* |
| right | `Vector3` | Shorthand for writing vector3(1, 0, 0). *(read-only)* |
| forward | `Vector3` | Shorthand for writing vector3(0, 0, -1). *(read-only)* |
| back | `Vector3` | Shorthand for writing vector3(0, 0, 1). *(read-only)* |
| positive_infinity | `Vector3` | Shorthand for writing vector3(inf, inf, inf). *(read-only)* |
| negative_infinity | `Vector3` | Shorthand for writing vector3(-inf, -inf, -inf). *(read-only)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `static vector3.angle(a: Vector3, b: Vector3) → float` | Return the angle in degrees between two vectors. |
| `static vector3.clamp_magnitude(v: Vector3, max_length: float) → Vector3` | Return a copy of the vector with its magnitude clamped. |
| `static vector3.cross(a: Vector3, b: Vector3) → Vector3` | Return the cross product of two vectors. |
| `static vector3.distance(a: Vector3, b: Vector3) → float` | Return the distance between two points. |
| `static vector3.dot(a: Vector3, b: Vector3) → float` | Return the dot product of two vectors. |
| `static vector3.lerp(a: Vector3, b: Vector3, t: float) → Vector3` | Linearly interpolate between two vectors. |
| `static vector3.lerp_unclamped(a: Vector3, b: Vector3, t: float) → Vector3` | Linearly interpolate between two vectors without clamping t. |
| `static vector3.max(a: Vector3, b: Vector3) → Vector3` | Return a vector made from the largest components of two vectors. |
| `static vector3.min(a: Vector3, b: Vector3) → Vector3` | Return a vector made from the smallest components of two vectors. |
| `static vector3.move_towards(current: Vector3, target: Vector3, max_delta: float) → Vector3` | Move current towards target by at most max_delta. |
| `static vector3.normalize(v: Vector3) → Vector3` | Return the vector with a magnitude of 1. |
| `static vector3.ortho_normalize(v1: Vector3, v2: Vector3, v3: Vector3) → Vector3` | Make vectors normalized and orthogonal to each other. |
| `static vector3.project(v: Vector3, on_normal: Vector3) → Vector3` | Project a vector onto another vector. |
| `static vector3.project_on_plane(v: Vector3, plane_normal: Vector3) → Vector3` | Project a vector onto a plane defined by its normal. |
| `static vector3.reflect(in_dir: Vector3, normal: Vector3) → Vector3` | Reflect a vector off the plane defined by a normal. |
| `static vector3.rotate_towards(current: Vector3, target: Vector3, max_radians: float, max_mag: float) → Vector3` | Rotate current towards target, limited by max angle and magnitude. |
| `static vector3.scale(a: Vector3, b: Vector3) → Vector3` | Multiply two vectors component-wise. |
| `static vector3.signed_angle(from_v: Vector3, to_v: Vector3, axis: Vector3) → float` | Return the signed angle in degrees between two vectors around an axis. |
| `static vector3.slerp(a: Vector3, b: Vector3, t: float) → Vector3` | Spherically interpolate between two vectors. |
| `static vector3.slerp_unclamped(a: Vector3, b: Vector3, t: float) → Vector3` | Spherically interpolate between two vectors without clamping t. |
| `static vector3.smooth_damp(current: Vector3, target: Vector3, current_velocity: Vector3, smooth_time: float, max_speed: float, delta_time: float) → Vector3` | Gradually change a vector towards a desired goal over time. |
| `static vector3.magnitude(v: Vector3) → float` | Return the length of the vector. |
| `static vector3.sqr_magnitude(v: Vector3) → float` | Return the squared length of the vector. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine.math import vector3

# Create positions
origin = vector3(0, 0, 0)
target = vector3(10, 5, 3)

# Direction and distance
direction = vector3.normalize(target - origin)
dist = vector3.distance(origin, target)

# Cross product — compute a surface normal from two edge vectors
edge_a = vector3(1, 0, 0)
edge_b = vector3(0, 1, 0)
normal = vector3.normalize(vector3.cross(edge_a, edge_b))

# Smooth movement toward a target
current = vector3(0, 0, 0)
current = vector3.lerp(current, target, 0.1)

# Use built-in direction constants
forward = vector3.forward   # (0, 0, 1)
up      = vector3.up         # (0, 1, 0)
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [vector2](vector2.md) — 2D vector operations
- [vector4](vector4.md) — 4D vectors for colors and homogeneous coordinates
- [Transform](Transform.md) — uses vector3 for position, rotation, and scale
- [GameObject](GameObject.md)

<!-- USER CONTENT END -->
