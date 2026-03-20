# Light

<div class="class-info">
class in <b>InfEngine.components.builtin</b>
</div>

**Inherits from:** [BuiltinComponent](Component.md)

## Description

A Light component that illuminates the scene.

<!-- USER CONTENT START --> description

Light illuminates the scene, affecting how [Materials](Material.md) and [MeshRenderers](MeshRenderer.md) appear. InfEngine supports three light types: directional lights (type 0) for sun-like parallel rays, point lights (type 1) that emit in all directions from a position, and spot lights (type 2) that emit in a cone.

Key properties include `color` and `intensity` for brightness, `range` for point and spot falloff distance, and `spot_angle` for the cone width of spot lights. Shadows can be toggled per light via the `shadows` property — set it to enable shadow mapping for that light source.

A scene typically has one directional light as the main sunlight, supplemented by point and spot lights for localized illumination. Adjust `shadow_strength` and `shadow_bias` to fine-tune shadow quality and reduce artifacts.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| light_type | `int` | The type of light (Directional, Point, or Spot). |
| color | `List[float]` | The color of the light. |
| intensity | `float` | The brightness of the light. |
| range | `float` | The range of the light in world units. |
| spot_angle | `float` | The inner cone angle of the spot light in degrees. |
| outer_spot_angle | `float` | The outer cone angle of the spot light in degrees. |
| shadows | `int` | The shadow casting mode of the light. |
| shadow_strength | `float` | The strength of the shadows cast by this light. |
| shadow_bias | `float` | Bias value to reduce shadow acne artifacts. |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Public Methods

| Method | Description |
|------|------|
| `get_light_view_matrix() → Any` | Return the light's view matrix for shadow mapping. |
| `get_light_projection_matrix(shadow_extent: float = ..., near_plane: float = ..., far_plane: float = ...) → Any` | Return the light's projection matrix for shadow mapping. |
| `serialize() → str` | Serialize the component to a JSON string. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## Lifecycle Methods

| Method | Description |
|------|------|
| `on_draw_gizmos_selected() → None` | Draw a type-specific gizmo when the light is selected. |

<!-- USER CONTENT START --> lifecycle_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.math import vector3, vector4

class LightSetup(InfComponent):
    def start(self):
        light = self.game_object.get_cpp_component("Light")
        if not light:
            light = self.game_object.add_component("Light")

        # Configure as a directional sunlight
        light.light_type = 0  # directional
        light.color = vector4(1.0, 0.95, 0.8, 1.0)  # warm white
        light.intensity = 1.2
        light.shadows = 1  # enable shadows
        light.shadow_strength = 0.8

        # Point the light downward at an angle
        self.transform.rotate(vector3(50, -30, 0))
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Camera](Camera.md)
- [Material](Material.md)
- [MeshRenderer](MeshRenderer.md)
- [GameObject](GameObject.md)

<!-- USER CONTENT END -->
