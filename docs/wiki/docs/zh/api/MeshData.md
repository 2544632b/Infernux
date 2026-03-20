# MeshData

<div class="class-info">
类位于 <b>InfEngine.core</b>
</div>

## 描述

网格数据，包含顶点、索引和属性。

<!-- USER CONTENT START --> description

MeshData 保存定义三维几何体的顶点和索引数据——包括位置、法线、UV 坐标、颜色、切线和三角形索引。它是 [MeshRenderer](MeshRenderer.md) 用于在屏幕上绘制物体的数据资源。

通过 `add_vertex()` 和 `add_triangle()` 以编程方式创建网格，或使用 `MeshData.cube()` 和 `MeshData.plane()` 生成内置基础体。也可以通过 `get_positions()`、`get_normals()` 和 `get_uvs()` 读取现有网格的顶点数据。

MeshData 支持通过 `to_numpy_positions()`、`to_numpy_normals()` 和 `to_numpy_indices()` 导出为 NumPy 数组，便于高效批量处理和分析几何数据。

<!-- USER CONTENT END -->

## 构造函数

| 签名 | 描述 |
|------|------|
| `MeshData.__init__() → None` | Create an empty mesh data container. |

<!-- USER CONTENT START --> constructors

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| vertex_count | `int` | 顶点数量。 *(只读)* |
| index_count | `int` | 索引数量。 *(只读)* |
| triangle_count | `int` | The number of triangles in the mesh. *(只读)* |
| vertices | `List[VertexData]` | The list of all vertices. *(只读)* |
| indices | `List[int]` | The list of all triangle indices. *(只读)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 公共方法

| 方法 | 描述 |
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

## 静态方法

| 方法 | 描述 |
|------|------|
| `static MeshData.cube() → MeshData` | Create a unit cube mesh centered at origin. |
| `static MeshData.plane(width: float = ..., depth: float = ...) → MeshData` | Create a plane mesh in the XZ plane. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 运算符

| 方法 | 返回值 |
|------|------|
| `__repr__() → str` | `str` |
| `__len__() → int` | `int` |

<!-- USER CONTENT START --> operators

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.core import MeshData

class MeshDemo(InfComponent):
    def start(self):
        # 创建内置立方体基础网格
        cube = MeshData.cube()
        print(f"立方体：{cube.vertex_count} 个顶点，{cube.triangle_count} 个三角形")

        # 以编程方式创建自定义三角形
        mesh = MeshData()
        mesh.add_vertex(position=(0, 0, 0), normal=(0, 1, 0), uv=(0, 0))
        mesh.add_vertex(position=(1, 0, 0), normal=(0, 1, 0), uv=(1, 0))
        mesh.add_vertex(position=(0, 0, 1), normal=(0, 1, 0), uv=(0, 1))
        mesh.add_triangle(0, 1, 2)

        # 检查几何数据
        positions = mesh.get_positions()
        for pos in positions:
            print(f"顶点：{pos}")
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [MeshRenderer 网格渲染器](MeshRenderer.md)
- [Material 材质](Material.md)
- [GameObject](GameObject.md)

<!-- USER CONTENT END -->
