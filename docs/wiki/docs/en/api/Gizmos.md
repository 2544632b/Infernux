# Gizmos

<div class="class-info">
class in <b>InfEngine.gizmos</b>
</div>

## Description

Draw visual debugging helpers in the Scene view.

<!-- USER CONTENT START --> description

Gizmos draws visual debugging aids in the Scene view. Use Gizmos inside the `on_draw_gizmos()` or `on_draw_gizmos_selected()` lifecycle methods of [InfComponent](InfComponent.md) to visualize boundaries, directions, and spatial relationships.

Set `Gizmos.color` before drawing to control the color of subsequent shapes. Available primitives include lines, rays, wire cubes, wire spheres, arcs, and camera frustums.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| color | `Tuple[float, float, float]` | The color used for drawing gizmos. *(read-only)* |
| matrix | `Optional[List[float]]` | The transformation matrix for gizmo drawing. *(read-only)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `Gizmos.draw_line(start: Vec3, end: Vec3) → None` | Draw a line from start to end in the Scene view. |
| `Gizmos.draw_ray(origin: Vec3, direction: Vec3) → None` | Draw a ray starting at origin in the given direction. |
| `Gizmos.draw_icon(position: Vec3, object_id: int, color: Optional[Tuple[float, float, float]] = ...) → None` | Draw an icon at the given world position. |
| `Gizmos.draw_wire_cube(center: Vec3, size: Vec3) → None` | Draw a wireframe cube in the Scene view. |
| `Gizmos.draw_wire_sphere(center: Vec3, radius: float, segments: int = ...) → None` | Draw a wireframe sphere in the Scene view. |
| `Gizmos.draw_frustum(position: Vec3, fov_deg: float, aspect: float, near: float, far: float, forward: Vec3 = ..., up: Vec3 = ..., right: Vec3 = ...) → None` | Draw a camera frustum wireframe in the Scene view. |
| `Gizmos.draw_wire_arc(center: Vec3, normal: Vec3, radius: float, start_angle_deg: float = ..., arc_deg: float = ..., segments: int = ...) → None` | Draw a wireframe arc in the Scene view. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.gizmos import Gizmos
from InfEngine.math import vector3

class GizmosDemo(InfComponent):
    attack_range: float = 5.0

    def on_draw_gizmos_selected(self):
        pos = self.transform.position

        # Red wire sphere for attack range
        Gizmos.color = (1, 0, 0)
        Gizmos.draw_wire_sphere(pos, self.attack_range)

        # Green ray showing forward direction
        Gizmos.color = (0, 1, 0)
        Gizmos.draw_ray(pos, self.transform.forward * 3)

        # Blue wire cube as a waypoint marker
        Gizmos.color = (0, 0, 1)
        Gizmos.draw_wire_cube(pos + vector3(0, 2, 0), vector3(1, 1, 1))

    def on_draw_gizmos(self):
        # Always-visible line between origin and this object
        Gizmos.color = (1, 1, 0)
        Gizmos.draw_line(vector3.zero, self.transform.position)
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Debug](Debug.md) — console logging
- [InfComponent](InfComponent.md) — `on_draw_gizmos()` and `on_draw_gizmos_selected()` lifecycle methods

<!-- USER CONTENT END -->
