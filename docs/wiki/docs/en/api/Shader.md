# Shader

<div class="class-info">
class in <b>InfEngine.core</b>
</div>

## Description

Static utility class for shader management.

Example::

    Shader.reload("pbr_lit")
    if Shader.is_loaded("pbr_lit", "vertex"):
        print("Ready")

<!-- USER CONTENT START --> description

Shader represents a compiled GPU shader program used by [Materials](Material.md). Shaders define how vertices are transformed and how pixels are colored. InfEngine's Vulkan backend compiles shaders to SPIR-V.

In most cases you work with shaders indirectly through [Material](Material.md) factory methods like `Material.create_lit()`, which automatically assign the appropriate shader. Use `Shader.is_loaded()` to check whether a shader is available, `Shader.reload()` for hot-reloading during development, and `Shader.load_spirv()` to load pre-compiled SPIR-V modules directly.

The two-stage pipeline uses a vertex shader to process geometry and a fragment shader to compute final pixel colors. Use `Shader.refresh_materials()` after reloading to update all materials that reference the changed shader.

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `Shader.is_loaded(name: str, shader_type: str = ...) → bool` | Check if a shader is loaded in the cache. |
| `Shader.invalidate(shader_id: str) → None` | Invalidate the shader program cache for hot-reload. |
| `Shader.reload(shader_id: str) → bool` | Invalidate cache and refresh all materials using this shader. |
| `Shader.refresh_materials(shader_id: str, engine: Optional[object] = ...) → bool` | Refresh all material pipelines that use a given shader. |
| `Shader.load_spirv(name: str, spirv_code: bytes, shader_type: str = ...) → None` | Load a SPIR-V shader module into the engine. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine.resources import Shader, Material

# Check if a shader is loaded
if Shader.is_loaded("pbr_lit"):
    print("PBR shader ready")

# Hot-reload a shader during development
Shader.reload("pbr_lit")

# Shaders are typically used via Material factory methods
mat = Material.create_lit()   # uses the lit shader internally
print(f"Shader: {mat.shader_name}")
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Material](Material.md)
- [Texture](Texture.md)
- [MeshRenderer](MeshRenderer.md)

<!-- USER CONTENT END -->
