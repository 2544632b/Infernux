# Shader

<div class="class-info">
类位于 <b>InfEngine.core</b>
</div>

## 描述

着色器程序资源。

<!-- USER CONTENT START --> description

Shader 表示 [Material](Material.md) 使用的已编译 GPU 着色器程序。着色器定义顶点如何变换以及像素如何着色。InfEngine 的 Vulkan 后端将着色器编译为 SPIR-V 格式。

通常通过 [Material](Material.md) 的工厂方法（如 `Material.create_lit()`）间接使用着色器，工厂方法会自动分配合适的着色器。使用 `Shader.is_loaded()` 检查着色器是否可用，`Shader.reload()` 在开发过程中热重载，`Shader.load_spirv()` 直接加载预编译的 SPIR-V 模块。

两阶段管线使用顶点着色器处理几何体，片段着色器计算最终像素颜色。重载后使用 `Shader.refresh_materials()` 更新所有引用该着色器的材质。

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `Shader.is_loaded(name: str, shader_type: str = ...) → bool` | Check if a shader is loaded in the cache. |
| `Shader.invalidate(shader_id: str) → None` | Invalidate the shader program cache for hot-reload. |
| `Shader.reload(shader_id: str) → bool` | Invalidate cache and refresh all materials using this shader. |
| `Shader.refresh_materials(shader_id: str, engine: Optional[object] = ...) → bool` | Refresh all material pipelines that use a given shader. |
| `Shader.load_spirv(name: str, spirv_code: bytes, shader_type: str = ...) → None` | Load a SPIR-V shader module into the engine. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine.resources import Shader, Material

# 检查着色器是否已加载
if Shader.is_loaded("pbr_lit"):
    print("PBR 着色器已就绪")

# 开发过程中热重载着色器
Shader.reload("pbr_lit")

# 着色器通常通过材质工厂方法使用
mat = Material.create_lit()   # 内部使用 Lit 着色器
print(f"着色器：{mat.shader_name}")
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Material 材质](Material.md)
- [Texture 纹理](Texture.md)
- [MeshRenderer 网格渲染器](MeshRenderer.md)

<!-- USER CONTENT END -->
