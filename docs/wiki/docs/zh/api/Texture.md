# Texture

<div class="class-info">
类位于 <b>InfEngine.core</b>
</div>

## 描述

纹理资源。

<!-- USER CONTENT START --> description

Texture 表示加载到 GPU 显存中的二维图像，供 [Material](Material.md) 使用以实现漫反射贴图、法线贴图等表面细节效果。通过 `Texture.load()` 从磁盘图像文件加载纹理。

加载后，可通过 `width`、`height` 和 `channels` 属性查看纹理尺寸。使用 `Material.set_texture_guid()` 将纹理指定到材质的 Uniform 上，使其在渲染时生效。像素数据可通过 `pixels_as_bytes()` 读取，或通过 `to_numpy()` 转换为 NumPy 数组用于图像处理。

引擎支持 PNG、JPG、BMP 和 TGA 等常见图像格式。还可以通过 `Texture.solid_color()`、`Texture.checkerboard()` 或 `Texture.from_memory()` 以编程方式创建纹理。

<!-- USER CONTENT END -->

## 构造函数

| 签名 | 描述 |
|------|------|
| `Texture.__init__(native: TextureData) → None` | Wrap an existing C++ TextureData. |

<!-- USER CONTENT START --> constructors

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| native | `TextureData` | The underlying C++ TextureData object. *(只读)* |
| width | `int` | 纹理宽度（像素）。 *(只读)* |
| height | `int` | 纹理高度（像素）。 *(只读)* |
| channels | `int` | Number of color channels (e.g. *(只读)* |
| name | `str` | 纹理名称。 *(只读)* |
| source_path | `str` | The file path the texture was loaded from. *(只读)* |
| size | `Tuple[int, int]` | ``(width, height)`` tuple. *(只读)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 公共方法

| 方法 | 描述 |
|------|------|
| `pixels_as_bytes() → bytes` | Get raw pixel data as bytes (row-major, RGBA or RGB). |
| `pixels_as_list() → list` | Get pixel data as a flat list of integers ``[0-255]``. |
| `to_numpy() → 'numpy.ndarray'` | Convert pixel data to a NumPy array ``(H, W, C)``, dtype ``uint8``. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `static Texture.load(file_path: str) → Optional[Texture]` | 从文件路径加载纹理。 |
| `static Texture.from_memory(data: bytes, width: int, height: int, channels: int = ..., name: str = ...) → Optional[Texture]` | Create a texture from raw pixel data in memory. |
| `static Texture.solid_color(width: int, height: int, r: int = ..., g: int = ..., b: int = ..., a: int = ...) → Optional[Texture]` | Create a solid color texture. |
| `static Texture.checkerboard(width: int, height: int, cell_size: int = ...) → Optional[Texture]` | Create a checkerboard pattern texture. |
| `static Texture.from_native(native: TextureData) → Texture` | Wrap an existing C++ TextureData. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 运算符

| 方法 | 返回值 |
|------|------|
| `__repr__() → str` | `str` |

<!-- USER CONTENT START --> operators

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.resources import Texture, Material

class TextureDemo(InfComponent):
    def start(self):
        # 从磁盘加载纹理
        tex = Texture.load("textures/stone_diffuse.png")
        if tex:
            print(f"已加载：{tex.width}x{tex.height}，{tex.channels} 通道")

            # 将纹理应用到材质
            mat = Material.create_lit()
            mat.set_texture_guid("_BaseMap", tex.name)

            renderer = self.game_object.get_cpp_component("MeshRenderer")
            if renderer:
                renderer.render_material = mat

        # 以编程方式创建纯红色纹理
        red_tex = Texture.solid_color(64, 64, r=255, g=0, b=0)
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Material 材质](Material.md)
- [Shader 着色器](Shader.md)
- [MeshRenderer 网格渲染器](MeshRenderer.md)

<!-- USER CONTENT END -->
