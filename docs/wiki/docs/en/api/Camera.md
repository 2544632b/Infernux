# Camera

<div class="class-info">
class in <b>InfEngine.components.builtin</b>
</div>

**Inherits from:** [BuiltinComponent](Component.md)

## Description

A Camera component that renders a view of the scene.

<!-- USER CONTENT START --> description

Camera is the component that renders a view of the scene to the screen. It operates in either perspective mode (realistic 3D depth) or orthographic mode (no depth foreshortening, suitable for 2D or technical views). Field of view, near and far clipping planes, and viewport rectangle control what geometry is visible.

When multiple cameras exist, the `depth` property determines rendering order — cameras with lower depth render first, enabling layered effects such as a gameplay camera beneath a UI overlay camera. Use coordinate conversion methods like `screen_to_world_point()` and `screen_point_to_ray()` to translate between screen pixels and 3D world positions for picking and interaction.

For advanced rendering, read the `view_matrix` and `projection_matrix` properties directly or modify clear flags and background color to control how the frame buffer is prepared before drawing.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| projection_mode | `int` | The projection mode (0 = Perspective, 1 = Orthographic). |
| field_of_view | `float` | The vertical field of view in degrees. |
| orthographic_size | `float` | Half-size of the camera in orthographic mode. |
| aspect_ratio | `float` | The aspect ratio of the camera (width / height). *(read-only)* |
| near_clip | `float` | The near clipping plane distance. |
| far_clip | `float` | The far clipping plane distance. |
| depth | `float` | The rendering order of the camera. |
| culling_mask | `int` | The layer mask used for culling objects. *(read-only)* |
| clear_flags | `int` | How the camera clears the background before rendering. |
| background_color | `List[float]` | The background color used when clear flags is set to solid color. |
| pixel_width | `int` | The width of the camera's render target in pixels. *(read-only)* |
| pixel_height | `int` | The height of the camera's render target in pixels. *(read-only)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Public Methods

| Method | Description |
|------|------|
| `screen_to_world_point(x: float, y: float, depth: float = ...) → Optional[Tuple[float, float, float]]` | Convert a screen-space point to world coordinates. |
| `world_to_screen_point(x: float, y: float, z: float) → Optional[Tuple[float, float]]` | Convert a world-space point to screen coordinates. |
| `screen_point_to_ray(x: float, y: float) → Optional[Tuple[Tuple[float, float, float], Tuple[float, float, float]]]` | Cast a ray from a screen-space point into the scene. |
| `serialize() → str` | Serialize the component to a JSON string. |
| `deserialize(json_str: str) → bool` | Deserialize the component from a JSON string. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## Lifecycle Methods

| Method | Description |
|------|------|
| `on_draw_gizmos_selected() → None` | Draw the camera frustum gizmo when selected in the editor. |

<!-- USER CONTENT START --> lifecycle_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent, serialized_field

class CameraSetup(InfComponent):
    def start(self):
        cam = self.game_object.get_cpp_component("Camera")
        if not cam:
            return

        # Configure a perspective camera
        cam.field_of_view = 60.0
        cam.near_clip = 0.3
        cam.far_clip = 500.0
        cam.depth = 0  # renders first

    def update(self, delta_time: float):
        cam = self.game_object.get_cpp_component("Camera")

        # Convert screen center to a world-space ray
        ray = cam.screen_point_to_ray(960.0, 540.0)
        if ray:
            origin, direction = ray
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [GameObject](GameObject.md)
- [Transform](Transform.md)
- [Light](Light.md)
- [MeshRenderer](MeshRenderer.md)

<!-- USER CONTENT END -->
