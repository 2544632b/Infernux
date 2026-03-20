# Camera

<div class="class-info">
类位于 <b>InfEngine.components.builtin</b>
</div>

**继承自:** [BuiltinComponent](Component.md)

## 描述

渲染场景视图的摄像机组件。

<!-- USER CONTENT START --> description

Camera 是将场景视图渲染到屏幕的组件。它支持透视模式（真实三维纵深）和正交模式（无透视缩短，适合二维或技术视图）。视场角、近远裁剪面和视口矩形共同控制可见的几何体范围。

当存在多个摄像机时，`depth` 属性决定渲染顺序——深度值较小的摄像机先渲染，从而实现分层效果，例如在游戏摄像机之上叠加 UI 覆盖摄像机。使用 `screen_to_world_point()` 和 `screen_point_to_ray()` 等坐标转换方法，可在屏幕像素与三维世界坐标之间转换，用于拾取和交互。

如需高级渲染控制，可直接读取 `view_matrix` 和 `projection_matrix` 属性，或修改清除标志和背景颜色以控制绘制前帧缓冲区的准备方式。

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| projection_mode | `int` | 投影模式（0=透视，1=正交）。 |
| field_of_view | `float` | 垂直视野角度（度）。 |
| orthographic_size | `float` | 正交模式下摄像机的半尺寸。 |
| aspect_ratio | `float` | 摄像机宽高比（宽/高）。 *(只读)* |
| near_clip | `float` | 近裁剪面距离。 |
| far_clip | `float` | 远裁剪面距离。 |
| depth | `float` | 摄像机渲染顺序。 |
| culling_mask | `int` | 用于剔除对象的图层遮罩。 *(只读)* |
| clear_flags | `int` | 摄像机渲染前清除背景的方式。 |
| background_color | `List[float]` | 清除标志设为纯色时使用的背景颜色。 |
| pixel_width | `int` | 渲染目标宽度（像素）。 *(只读)* |
| pixel_height | `int` | 渲染目标高度（像素）。 *(只读)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 公共方法

| 方法 | 描述 |
|------|------|
| `screen_to_world_point(x: float, y: float, depth: float = ...) → Optional[Tuple[float, float, float]]` | 将屏幕空间坐标转换为世界坐标。 |
| `world_to_screen_point(x: float, y: float, z: float) → Optional[Tuple[float, float]]` | 将世界空间坐标转换为屏幕坐标。 |
| `screen_point_to_ray(x: float, y: float) → Optional[Tuple[Tuple[float, float, float], Tuple[float, float, float]]]` | 从屏幕空间坐标向场景发出射线。 |
| `serialize() → str` | Serialize the component to a JSON string. |
| `deserialize(json_str: str) → bool` | Deserialize the component from a JSON string. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## 生命周期方法

| 方法 | 描述 |
|------|------|
| `on_draw_gizmos_selected() → None` | 选中时绘制摄像机视锥 Gizmo。 |

<!-- USER CONTENT START --> lifecycle_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent, serialized_field

class CameraSetup(InfComponent):
    def start(self):
        cam = self.game_object.get_cpp_component("Camera")
        if not cam:
            return

        # 配置透视摄像机
        cam.field_of_view = 60.0
        cam.near_clip = 0.3
        cam.far_clip = 500.0
        cam.depth = 0  # 最先渲染

    def update(self, delta_time: float):
        cam = self.game_object.get_cpp_component("Camera")

        # 将屏幕中心转换为世界空间射线
        ray = cam.screen_point_to_ray(960.0, 540.0)
        if ray:
            origin, direction = ray
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [GameObject](GameObject.md)
- [Transform](Transform.md)
- [Light 灯光](Light.md)
- [MeshRenderer 网格渲染器](MeshRenderer.md)

<!-- USER CONTENT END -->
