# Gizmos

<div class="class-info">
类位于 <b>InfEngine.gizmos</b>
</div>

## 描述

在场景视图中绘制调试可视化图形的工具类。

<!-- USER CONTENT START --> description

Gizmos 在场景视图中绘制可视化调试辅助图形。在 [InfComponent](InfComponent.md) 的 `on_draw_gizmos()` 或 `on_draw_gizmos_selected()` 生命周期方法中使用 Gizmos 来可视化边界、方向和空间关系。

在绘制前设置 `Gizmos.color` 来控制后续图形的颜色。可用的基本图元包括线段、射线、线框立方体、线框球体、弧线和摄像机视锥体。

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| color | `Tuple[float, float, float]` | 下一次绘制操作使用的颜色。 *(只读)* |
| matrix | `Optional[List[float]]` | The transformation matrix for gizmo drawing. *(只读)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `Gizmos.draw_line(start: Vec3, end: Vec3) → None` | 绘制一条线段。 |
| `Gizmos.draw_ray(origin: Vec3, direction: Vec3) → None` | 绘制一条射线。 |
| `Gizmos.draw_icon(position: Vec3, object_id: int, color: Optional[Tuple[float, float, float]] = ...) → None` | 在指定位置绘制图标。 |
| `Gizmos.draw_wire_cube(center: Vec3, size: Vec3) → None` | 绘制线框立方体。 |
| `Gizmos.draw_wire_sphere(center: Vec3, radius: float, segments: int = ...) → None` | 绘制线框球体。 |
| `Gizmos.draw_frustum(position: Vec3, fov_deg: float, aspect: float, near: float, far: float, forward: Vec3 = ..., up: Vec3 = ..., right: Vec3 = ...) → None` | 绘制视锥体。 |
| `Gizmos.draw_wire_arc(center: Vec3, normal: Vec3, radius: float, start_angle_deg: float = ..., arc_deg: float = ..., segments: int = ...) → None` | Draw a wireframe arc in the Scene view. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.gizmos import Gizmos
from InfEngine.math import vector3

class GizmosDemo(InfComponent):
    attack_range: float = 5.0

    def on_draw_gizmos_selected(self):
        pos = self.transform.position

        # 红色线框球体表示攻击范围
        Gizmos.color = (1, 0, 0)
        Gizmos.draw_wire_sphere(pos, self.attack_range)

        # 绿色射线表示前方方向
        Gizmos.color = (0, 1, 0)
        Gizmos.draw_ray(pos, self.transform.forward * 3)

        # 蓝色线框立方体作为路点标记
        Gizmos.color = (0, 0, 1)
        Gizmos.draw_wire_cube(pos + vector3(0, 2, 0), vector3(1, 1, 1))

    def on_draw_gizmos(self):
        # 始终可见的从原点到此对象的线段
        Gizmos.color = (1, 1, 0)
        Gizmos.draw_line(vector3.zero, self.transform.position)
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Debug](Debug.md) — 控制台日志
- [InfComponent](InfComponent.md) — `on_draw_gizmos()` 和 `on_draw_gizmos_selected()` 生命周期方法

<!-- USER CONTENT END -->
