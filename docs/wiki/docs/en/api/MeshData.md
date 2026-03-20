# MeshData

<div class="class-info">
class in <b>InfEngine.core</b>
</div>

## Description

Python-side mesh data container.

Example::

    mesh = MeshData()
    mesh.add_vertex(position=(0, 0, 0), normal=(0, 1, 0), uv=(0, 0))
    mesh.add_vertex(position=(1, 0, 0), normal=(0, 1, 0), uv=(1, 0))
    mesh.add_vertex(position=(0, 0, 1), normal=(0, 1, 0), uv=(0, 1))
    mesh.add_triangle(0, 1, 2)

    # Primitives
    mesh = MeshData.cube()
    mesh = MeshData.plane()

<!-- USER CONTENT START --> description

MeshData holds the vertex and index data that defines 3D geometry — positions, normals, UVs, colors, tangents, and triangle indices. It is the data asset consumed by [MeshRenderer](MeshRenderer.md) to draw objects on screen.

Create meshes procedurally with `add_vertex()` and `add_triangle()`, or generate built-in primitives with `MeshData.cube()` and `MeshData.plane()`. You can also read vertex data from an existing mesh using `get_positions()`, `get_normals()`, and `get_uvs()`.

MeshData supports NumPy export via `to_numpy_positions()`, `to_numpy_normals()`, and `to_numpy_indices()` for efficient batch processing and analysis of geometry data.

<!-- USER CONTENT END -->

## Constructors

| Signature | Description |
|------|------|
| `MeshData.__init__() → None` | Create an empty mesh data container. |

<!-- USER CONTENT START --> constructors

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| vertex_count | `int` | The number of vertices in the mesh. *(read-only)* |
| index_count | `int` | The number of indices in the mesh. *(read-only)* |
| triangle_count | `int` | The number of triangles in the mesh. *(read-only)* |
| vertices | `List[VertexData]` | The list of all vertices. *(read-only)* |
| indices | `List[int]` | The list of all triangle indices. *(read-only)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Public Methods

| Method | Description |
|------|------|
| `add_vertex(position: Tuple[float, float, float], normal: Tuple[float, float, float] = ..., uv: Tuple[float, float] = ..., color: Tuple[float, float, float] = ..., tangent: Tuple[float, float, float, float] = ...) → int` | Add a vertex and return its index. |
| `add_triangle(i0: int, i1: int, i2: int) → None` | Add a triangle by three vertex indices. |
| `add_quad(i0: int, i1: int, i2: int, i3: int) → None` | Add a quad as two triangles. |
| `clear() → None` | Remove all vertices and indices. |
| `get_positions() → List[Tuple[float, float, float]]` | Get all vertex positions as a list of (X, Y, Z) tuples. |
| `get_normals() → List[Tuple[float, float, float]]` | Get all vertex normals as a list of (X, Y, Z) tuples. |
| `get_uvs() → List[Tuple[float, float]]` | Get all UV coordinates as a list of (U, V) tuples. |
| `get_colors() → List[Tuple[float, float, float]]` | Get all vertex colors as a list of (R, G, B) tuples. |
| `to_numpy_positions() → 'numpy.ndarray'` | Get vertex positions as a NumPy array of shape (N, 3). |
| `to_numpy_normals() → 'numpy.ndarray'` | Get vertex normals as a NumPy array of shape (N, 3). |
| `to_numpy_indices() → 'numpy.ndarray'` | Get triangle indices as a NumPy array. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `static MeshData.cube() → MeshData` | Create a unit cube mesh centered at origin. |
| `static MeshData.plane(width: float = ..., depth: float = ...) → MeshData` | Create a plane mesh in the XZ plane. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Operators

| Method | Returns |
|------|------|
| `__repr__() → str` | `str` |
| `__len__() → int` | `int` |

<!-- USER CONTENT START --> operators

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.core import MeshData

class MeshDemo(InfComponent):
    def start(self):
        # Create a built-in cube primitive
        cube = MeshData.cube()
        print(f"Cube: {cube.vertex_count} vertices, {cube.triangle_count} triangles")

        # Create a custom triangle procedurally
        mesh = MeshData()
        mesh.add_vertex(position=(0, 0, 0), normal=(0, 1, 0), uv=(0, 0))
        mesh.add_vertex(position=(1, 0, 0), normal=(0, 1, 0), uv=(1, 0))
        mesh.add_vertex(position=(0, 0, 1), normal=(0, 1, 0), uv=(0, 1))
        mesh.add_triangle(0, 1, 2)

        # Inspect geometry data
        positions = mesh.get_positions()
        for pos in positions:
            print(f"Vertex: {pos}")
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [MeshRenderer](MeshRenderer.md)
- [Material](Material.md)
- [GameObject](GameObject.md)

<!-- USER CONTENT END -->
