# Material

<div class="class-info">
类位于 <b>InfEngine.core</b>
</div>

## 描述

材质类。控制物体的视觉外观。

<!-- USER CONTENT START --> description

Material 定义渲染几何体的视觉外观，控制着色、颜色、纹理和渲染状态。每个 Material 引用一个 [Shader](Shader.md) 程序，并提供一组属性（Uniform）供着色器使用。

使用工厂方法 `Material.create_lit()` 创建基于物理的渲染材质，或使用 `Material.create_unlit()` 创建无光照的纯色材质。通过类型化方法设置 Uniform 值：`set_color()` 设置 RGBA 颜色，`set_float()` 设置数值参数，`set_texture_guid()` 设置纹理贴图，`set_vector3()` / `set_vector4()` 设置向量值。

渲染状态——如剪除模式、混合模式、深度测试和表面类型——通过专用属性进行配置。材质被指定到 [MeshRenderer](MeshRenderer.md) 后才会生效。

<!-- USER CONTENT END -->

## 构造函数

| 签名 | 描述 |
|------|------|
| `Material.__init__(native: InfMaterial) → None` | Wrap an existing C++ InfMaterial. |

<!-- USER CONTENT START --> constructors

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| native | `InfMaterial` | 底层 C++ InfMaterial 对象。 *(只读)* |
| name | `str` | 材质的显示名称。 |
| guid | `str` | 材质的全局唯一标识符。 *(只读)* |
| render_queue | `int` | 渲染队列优先级，用于绘制排序。 |
| shader_name | `str` | 材质使用的着色器程序名称。 |
| vert_shader_name | `str` | 顶点着色器名称。 |
| frag_shader_name | `str` | 片段着色器名称。 |
| is_builtin | `bool` | 是否为引擎内置材质。 *(只读)* |
| render_state_overrides | `int` | 应用于此材质的渲染状态覆盖位掩码。 |
| cull_mode | `int` | 面剔除模式（0=无，1=正面，2=背面）。 |
| depth_write_enable | `bool` | 是否启用深度缓冲写入。 |
| depth_test_enable | `bool` | 是否启用深度测试。 |
| depth_compare_op | `int` | 深度比较运算符。 |
| blend_enable | `bool` | 是否启用 Alpha 混合。 |
| surface_type | `str` | 表面类型（'opaque' 或 'transparent'）。 |
| alpha_clip_enabled | `bool` | 是否启用 Alpha 裁剪。 |
| alpha_clip_threshold | `float` | Alpha 裁剪阈值。 |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 公共方法

| 方法 | 描述 |
|------|------|
| `dispose() → None` | 释放底层原生材质资源。 |
| `set_shader(shader_name: str) → None` | 设置材质使用的着色器。 |
| `set_float(name: str, value: float) → None` | 设置浮点数 uniform 属性。 |
| `set_int(name: str, value: int) → None` | 设置整数 uniform 属性。 |
| `set_color(name: str, r: float, g: float, b: float, a: float = ...) → None` | 设置颜色 uniform 属性。 |
| `set_vector2(name: str, x: float, y: float) → None` | 设置二维向量 uniform 属性。 |
| `set_vector3(name: str, x: float, y: float, z: float) → None` | 设置三维向量 uniform 属性。 |
| `set_vector4(name: str, x: float, y: float, z: float, w: float) → None` | 设置四维向量 uniform 属性。 |
| `set_texture_guid(name: str, texture_guid: str) → None` | 通过 GUID 将纹理分配给采样器槽。 |
| `clear_texture(name: str) → None` | 移除分配给采样器槽的纹理。 |
| `get_float(name: str, default: float = ...) → float` | 获取浮点数属性值。 |
| `get_int(name: str, default: int = ...) → int` | 获取整数属性值。 |
| `get_color(name: str) → Tuple[float, float, float, float]` | 获取颜色属性（返回 RGBA 元组）。 |
| `get_vector2(name: str) → Tuple[float, float]` | 获取二维向量属性。 |
| `get_vector3(name: str) → Tuple[float, float, float]` | 获取三维向量属性。 |
| `get_vector4(name: str) → Tuple[float, float, float, float]` | 获取四维向量属性。 |
| `get_texture(name: str) → Optional[str]` | 获取采样器槽中纹理的 GUID。 |
| `has_property(name: str) → bool` | 检查着色器属性是否存在。 |
| `get_property(name: str) → Any` | 按名称获取着色器属性值。 |
| `get_all_properties() → dict` | 获取所有着色器属性的字典。 |
| `to_dict() → dict` | 将材质序列化为字典。 |
| `save(file_path: str) → bool` | 将材质保存到文件。 |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `static Material.create_lit(name: str = ...) → Material` | 使用默认 PBR 着色器创建新材质。 |
| `static Material.create_unlit(name: str = ...) → Material` | 使用无光照着色器创建新材质。 |
| `static Material.from_native(native: InfMaterial) → Material` | 封装现有的 C++ InfMaterial 实例。 |
| `static Material.load(file_path: str) → Optional[Material]` | 从文件路径加载材质。 |
| `static Material.get(name: str) → Optional[Material]` | 按名称获取缓存的材质。 |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 运算符

| 方法 | 返回值 |
|------|------|
| `__repr__() → str` | `str` |
| `__eq__(other: object) → bool` | `bool` |
| `__hash__() → int` | `int` |

<!-- USER CONTENT START --> operators

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.resources import Material

class MaterialDemo(InfComponent):
    def start(self):
        # 创建光照（PBR）材质
        mat = Material.create_lit()
        mat.set_color("_BaseColor", 1.0, 0.3, 0.3, 1.0)  # 红色调
        mat.set_float("_Metallic", 0.0)
        mat.set_float("_Roughness", 0.4)

        # 应用到渲染器
        renderer = self.game_object.get_cpp_component("MeshRenderer")
        if renderer:
            renderer.render_material = mat

        # 创建无光照材质，适用于 UI 元素
        unlit = Material.create_unlit()
        unlit.set_color("_BaseColor", 0.0, 1.0, 0.0, 1.0)
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Shader 着色器](Shader.md)
- [Texture 纹理](Texture.md)
- [MeshRenderer 网格渲染器](MeshRenderer.md)
- [Light 灯光](Light.md)

<!-- USER CONTENT END -->
