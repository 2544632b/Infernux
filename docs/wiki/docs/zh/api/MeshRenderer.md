# MeshRenderer

<div class="class-info">
类位于 <b>InfEngine.components.builtin</b>
</div>

**继承自:** [BuiltinComponent](Component.md)

## 描述

使用网格和材质渲染 3D 几何体的组件。

<!-- USER CONTENT START --> description

MeshRenderer 是负责在场景中绘制三维几何体的组件。它将网格数据与 [Material](Material.md)（材质）结合，产生可见的对象。没有 MeshRenderer 的 [GameObject](GameObject.md) 虽然存在于场景层级中，但不会有任何视觉表现。

通过网格资产 GUID 指定网格，通过 `render_material` 或 `material_guid` 指定材质。`casts_shadows` 和 `receives_shadows` 属性控制阴影交互。MeshRenderer 读取对象的 [Transform](Transform.md) 来确定网格在世界空间中的位置。

对于需要多种材质的对象（例如不同的子网格），使用 `set_material_slot_count()` 和 `set_material()` 配置各个槽位。通过 `get_positions()`、`get_normals()` 和 `get_uvs()` 在运行时访问顶点数据。

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| casts_shadows | `bool` | Whether this renderer casts shadows. |
| receives_shadows | `bool` | Whether this renderer receives shadows. |
| render_material | `Any` | The primary material used for rendering. |
| material_guid | `str` | The asset GUID of the primary material. |
| material_count | `int` | The number of material slots on this renderer. *(只读)* |
| has_mesh_asset | `bool` | Whether a mesh asset is assigned to this renderer. *(只读)* |
| mesh_asset_guid | `str` | The asset GUID of the assigned mesh. *(只读)* |
| mesh_name | `str` | The name of the assigned mesh. *(只读)* |
| vertex_count | `int` | The number of vertices in the mesh. *(只读)* |
| index_count | `int` | The number of indices in the mesh. *(只读)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 公共方法

| 方法 | 描述 |
|------|------|
| `has_render_material() → bool` | Return whether a render material is currently assigned. |
| `get_effective_material(slot: int = ...) → Any` | Return the effective material for the given slot, including fallbacks. |
| `get_material(slot: int) → Any` | Return the material at the specified slot index. |
| `set_material(slot: int, guid: str) → None` | Assign a material to the specified slot by asset GUID. |
| `get_material_guids() → List[str]` | Return the list of material GUIDs for all slots. |
| `set_materials(guids: List[str]) → None` | Set all material slots from a list of asset GUIDs. |
| `set_material_slot_count(count: int) → None` | Set the number of material slots on this renderer. |
| `has_inline_mesh() → bool` | Return whether the renderer has an inline (non-asset) mesh. |
| `get_mesh_asset() → Any` | Return the InfMesh asset object, or None. |
| `get_material_slot_names() → List[str]` | Return material slot names from the model file. |
| `get_submesh_infos() → List[Dict[str, Any]]` | Return info dicts for each submesh. |
| `get_positions() → List[Tuple[float, float, float]]` | Return the list of vertex positions. |
| `get_normals() → List[Tuple[float, float, float]]` | Return the list of vertex normals. |
| `get_uvs() → List[Tuple[float, float]]` | Return the list of UV coordinates. |
| `get_indices() → List[int]` | Return the list of triangle indices. |
| `serialize() → str` | Serialize the component to a JSON string. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.resources import Material

class MeshSetup(InfComponent):
    def start(self):
        renderer = self.game_object.get_cpp_component("MeshRenderer")
        if not renderer:
            renderer = self.game_object.add_component("MeshRenderer")

        # 创建并指定光照材质
        mat = Material.create_lit()
        mat.set_color("_BaseColor", 0.2, 0.6, 1.0, 1.0)
        renderer.render_material = mat

        # 配置阴影行为
        renderer.casts_shadows = True
        renderer.receives_shadows = True

        # 检查网格数据
        print(f"顶点数：{renderer.vertex_count}")
        print(f"索引数：{renderer.index_count}")
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Material 材质](Material.md)
- [MeshData 网格数据](MeshData.md)
- [Shader 着色器](Shader.md)
- [Transform](Transform.md)

<!-- USER CONTENT END -->
