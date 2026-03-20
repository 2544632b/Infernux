# Texture

<div class="class-info">
class in <b>InfEngine.core</b>
</div>

## Description

Pythonic wrapper around C++ TextureData.

Example::

    tex = Texture.load("textures/albedo.png")
    print(tex.width, tex.height, tex.channels)
    pixels = tex.pixels_as_bytes()

    import numpy as np
    arr = np.frombuffer(pixels, dtype=np.uint8).reshape(
        tex.height, tex.width, tex.channels
    )

<!-- USER CONTENT START --> description

Texture represents a 2D image loaded into GPU memory, used by [Materials](Material.md) for surface detail such as diffuse color maps, normal maps, and other effects. Textures are loaded from image files on disk using `Texture.load()`.

After loading, read the `width`, `height`, and `channels` properties to inspect the texture's dimensions. Assign a Texture to a material uniform with `Material.set_texture_guid()` to apply it during rendering. Pixel data can be read back via `pixels_as_bytes()` or converted to NumPy arrays with `to_numpy()` for image processing.

The engine supports common image formats including PNG, JPG, BMP, and TGA. You can also create textures procedurally via `Texture.solid_color()`, `Texture.checkerboard()`, or `Texture.from_memory()` with raw pixel data.

<!-- USER CONTENT END -->

## Constructors

| Signature | Description |
|------|------|
| `Texture.__init__(native: TextureData) → None` | Wrap an existing C++ TextureData. |

<!-- USER CONTENT START --> constructors

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| native | `TextureData` | The underlying C++ TextureData object. *(read-only)* |
| width | `int` | Width of the texture in pixels. *(read-only)* |
| height | `int` | Height of the texture in pixels. *(read-only)* |
| channels | `int` | Number of color channels (e.g. *(read-only)* |
| name | `str` | The display name of the texture. *(read-only)* |
| source_path | `str` | The file path the texture was loaded from. *(read-only)* |
| size | `Tuple[int, int]` | ``(width, height)`` tuple. *(read-only)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Public Methods

| Method | Description |
|------|------|
| `pixels_as_bytes() → bytes` | Get raw pixel data as bytes (row-major, RGBA or RGB). |
| `pixels_as_list() → list` | Get pixel data as a flat list of integers ``[0-255]``. |
| `to_numpy() → 'numpy.ndarray'` | Convert pixel data to a NumPy array ``(H, W, C)``, dtype ``uint8``. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `static Texture.load(file_path: str) → Optional[Texture]` | Load a texture from an image file (PNG, JPG, BMP, TGA). |
| `static Texture.from_memory(data: bytes, width: int, height: int, channels: int = ..., name: str = ...) → Optional[Texture]` | Create a texture from raw pixel data in memory. |
| `static Texture.solid_color(width: int, height: int, r: int = ..., g: int = ..., b: int = ..., a: int = ...) → Optional[Texture]` | Create a solid color texture. |
| `static Texture.checkerboard(width: int, height: int, cell_size: int = ...) → Optional[Texture]` | Create a checkerboard pattern texture. |
| `static Texture.from_native(native: TextureData) → Texture` | Wrap an existing C++ TextureData. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Operators

| Method | Returns |
|------|------|
| `__repr__() → str` | `str` |

<!-- USER CONTENT START --> operators

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.resources import Texture, Material

class TextureDemo(InfComponent):
    def start(self):
        # Load a texture from disk
        tex = Texture.load("textures/stone_diffuse.png")
        if tex:
            print(f"Loaded: {tex.width}x{tex.height}, {tex.channels} channels")

            # Apply the texture to a material
            mat = Material.create_lit()
            mat.set_texture_guid("_BaseMap", tex.name)

            renderer = self.game_object.get_cpp_component("MeshRenderer")
            if renderer:
                renderer.render_material = mat

        # Create a solid red texture procedurally
        red_tex = Texture.solid_color(64, 64, r=255, g=0, b=0)
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Material](Material.md)
- [Shader](Shader.md)
- [MeshRenderer](MeshRenderer.md)

<!-- USER CONTENT END -->
