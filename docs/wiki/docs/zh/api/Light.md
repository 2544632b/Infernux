# Light

<div class="class-info">
类位于 <b>InfEngine.components.builtin</b>
</div>

**继承自:** [BuiltinComponent](Component.md)

## 描述

为场景提供照明的光源组件。

<!-- USER CONTENT START --> description

Light 用于照亮场景，影响 [Material](Material.md) 和 [MeshRenderer](MeshRenderer.md) 的显示效果。InfEngine 支持三种灯光类型：平行光（类型 0）用于类似太阳的平行光线，点光源（类型 1）从一个位置向所有方向发射光线，聚光灯（类型 2）在锥形范围内发射光线。

主要属性包括控制亮度的 `color` 和 `intensity`，控制点光源和聚光灯衰减距离的 `range`，以及控制聚光灯锥形宽度的 `spot_angle`。每个灯光都可以通过 `shadows` 属性切换阴影——启用后将为该光源生成阴影贴图。

场景通常使用一个平行光作为主日光，再辅以点光源和聚光灯进行局部照明。调整 `shadow_strength` 和 `shadow_bias` 可微调阴影质量并减少伪影。

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| light_type | `int` | 光源类型（0=方向光，1=点光源，2=聚光灯）。 |
| color | `List[float]` | 光源颜色（RGB）。 |
| intensity | `float` | 光源强度。 |
| range | `float` | 点光源或聚光灯的照射范围。 |
| spot_angle | `float` | 聚光灯的锥角（度）。 |
| outer_spot_angle | `float` | The outer cone angle of the spot light in degrees. |
| shadows | `int` | The shadow casting mode of the light. |
| shadow_strength | `float` | 阴影强度。 |
| shadow_bias | `float` | 阴影偏移量。 |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 公共方法

| 方法 | 描述 |
|------|------|
| `get_light_view_matrix() → Any` | Return the light's view matrix for shadow mapping. |
| `get_light_projection_matrix(shadow_extent: float = ..., near_plane: float = ..., far_plane: float = ...) → Any` | Return the light's projection matrix for shadow mapping. |
| `serialize() → str` | Serialize the component to a JSON string. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## 生命周期方法

| 方法 | 描述 |
|------|------|
| `on_draw_gizmos_selected() → None` | Draw a type-specific gizmo when the light is selected. |

<!-- USER CONTENT START --> lifecycle_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.math import vector3, vector4

class LightSetup(InfComponent):
    def start(self):
        light = self.game_object.get_cpp_component("Light")
        if not light:
            light = self.game_object.add_component("Light")

        # 配置为平行光（太阳光）
        light.light_type = 0  # 平行光
        light.color = vector4(1.0, 0.95, 0.8, 1.0)  # 暖白色
        light.intensity = 1.2
        light.shadows = 1  # 启用阴影
        light.shadow_strength = 0.8

        # 将灯光向下倾斜一定角度
        self.transform.rotate(vector3(50, -30, 0))
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Camera 摄像机](Camera.md)
- [Material 材质](Material.md)
- [MeshRenderer 网格渲染器](MeshRenderer.md)
- [GameObject](GameObject.md)

<!-- USER CONTENT END -->
