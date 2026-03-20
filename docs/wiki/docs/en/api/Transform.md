# Transform

<div class="class-info">
class in <b>InfEngine</b>
</div>

**Inherits from:** [Component](Component.md)

## Description

Transform component — position, rotation, scale.

Follows Unity convention:
  - position / euler_angles → world space
  - local_position / local_euler_angles / local_scale → local (parent) space

<!-- USER CONTENT START --> description

Transform determines the position, rotation, and scale of a [GameObject](GameObject.md) in the scene. Every GameObject has exactly one Transform, and it cannot be removed. Transforms form a hierarchy: when a Transform has a parent, its `local_position`, `local_rotation`, and `local_scale` are relative to the parent. The `position` and `rotation` properties give world-space values.

Direction helpers — `forward`, `right`, and `up` — return the object's current orientation axes in world space, making it straightforward to implement movement and aiming. Use `translate()` and `rotate()` for incremental motion, or set `position` and `rotation` directly for teleportation and snapping.

The parent-child relationship is established through `set_parent()` on the [GameObject](GameObject.md). When the parent moves, all children move with it. Accessing `local_position` and `local_rotation` lets you offset children relative to their parent without worrying about world coordinates.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| position | `Vector3` | Position in world space (considering parent hierarchy). |
| euler_angles | `Vector3` | Rotation as Euler angles (degrees) in world space. |
| local_position | `Vector3` | Position in local (parent) space. |
| local_euler_angles | `Vector3` | Rotation as Euler angles (degrees) in local space. |
| local_scale | `Vector3` | Scale in local space. |
| lossy_scale | `Vector3` | Approximate world-space scale (read-only, like Unity lossyScale). *(read-only)* |
| forward | `Vector3` | Forward direction in world space (negative Z). *(read-only)* |
| right | `Vector3` | Right direction in world space (positive X). *(read-only)* |
| up | `Vector3` | Up direction in world space (positive Y). *(read-only)* |
| local_forward | `Vector3` | Forward direction in local space (negative Z). *(read-only)* |
| local_right | `Vector3` | Right direction in local space (positive X). *(read-only)* |
| local_up | `Vector3` | Up direction in local space (positive Y). *(read-only)* |
| rotation | `Tuple[float, float, float, float]` | World-space rotation as quaternion (x, y, z, w). |
| local_rotation | `Tuple[float, float, float, float]` | Local-space rotation as quaternion (x, y, z, w). |
| parent | `Optional[Transform]` | Parent Transform (None if root). |
| root | `Transform` | Topmost Transform in the hierarchy. *(read-only)* |
| child_count | `int` | Number of children. *(read-only)* |
| has_changed | `bool` | Has the transform changed since last reset? Unity: transform.hasChanged |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Public Methods

| Method | Description |
|------|------|
| `set_parent(parent: Optional[Transform], world_position_stays: bool = True) → None` | Set parent Transform. |
| `get_child(index: int) → Optional[Transform]` | Get child Transform by index. |
| `find(name: str) → Optional[Transform]` | Find child Transform by name (non-recursive). |
| `detach_children() → None` | Unparent all children. |
| `is_child_of(parent: Transform) → bool` | Is this transform a child of parent? Unity: transform.IsChildOf(parent) |
| `get_sibling_index() → int` | Get sibling index. |
| `set_sibling_index(index: int) → None` | Set sibling index. |
| `set_as_first_sibling() → None` | Move to first sibling. |
| `set_as_last_sibling() → None` | Move to last sibling. |
| `transform_point(point: Vector3) → Vector3` | Transform point from local to world space. |
| `inverse_transform_point(point: Vector3) → Vector3` | Transform point from world to local space. |
| `transform_direction(direction: Vector3) → Vector3` | Transform direction from local to world (rotation only). |
| `inverse_transform_direction(direction: Vector3) → Vector3` | Transform direction from world to local (rotation only). |
| `transform_vector(vector: Vector3) → Vector3` | Transform vector from local to world (with scale). |
| `inverse_transform_vector(vector: Vector3) → Vector3` | Transform vector from world to local (with scale). |
| `local_to_world_matrix() → List[float]` | Get local-to-world transformation matrix (16 floats, column-major). |
| `world_to_local_matrix() → List[float]` | Get world-to-local transformation matrix (16 floats, column-major). |
| `look_at(target: Vector3) → None` | Rotate to face a world-space target position. |
| `translate(delta: Vector3) → None` | Translate in world space. |
| `translate_local(delta: Vector3) → None` | Translate in local space (relative to own axes). |
| `rotate(euler: Vector3) → None` | Rotate by Euler angles (degrees) in local space. |
| `rotate_around(point: Vector3, axis: Vector3, angle: float) → None` | Rotate around a world-space point. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent, serialized_field
from InfEngine.math import vector3

class Mover(InfComponent):
    speed: float = serialized_field(default=3.0)
    rotation_speed: float = serialized_field(default=90.0)

    def update(self, delta_time: float):
        # Move forward in the object's facing direction
        self.transform.translate(self.transform.forward * self.speed * delta_time)

        # Rotate around the Y axis
        self.transform.rotate(vector3(0, self.rotation_speed * delta_time, 0))

        # Read world-space position
        pos = self.transform.position
        if pos.y < -10:
            # Reset position if fallen off the map
            self.transform.position = vector3(0, 5, 0)

        # Access local-space values relative to parent
        local_pos = self.transform.local_position
        local_pos.y = 1.0  # maintain a fixed height offset from parent
        self.transform.local_position = local_pos
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [GameObject](GameObject.md)
- [vector3](vector3.md)
- [Component](Component.md)

<!-- USER CONTENT END -->
