# MeshRenderer

<div class="class-info">
class in <b>InfEngine.components.builtin</b>
</div>

**Inherits from:** [BuiltinComponent](Component.md)

## Description

Renders a mesh with assigned materials.

<!-- USER CONTENT START --> description

MeshRenderer is the component responsible for drawing 3D geometry in the scene. It combines mesh data with a [Material](Material.md) to produce a visible object. Without a MeshRenderer, a [GameObject](GameObject.md) exists in the scene hierarchy but has no visual representation.

Assign a mesh through the mesh asset GUID and a material through `render_material` or `material_guid`. The `casts_shadows` and `receives_shadows` properties control shadow interaction. MeshRenderer reads the object's [Transform](Transform.md) to position the mesh in world space.

For objects that require multiple materials (e.g., different sub-meshes), use `set_material_slot_count()` and `set_material()` to configure individual slots. Access vertex data at runtime through `get_positions()`, `get_normals()`, and `get_uvs()`.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| casts_shadows | `bool` | Whether this renderer casts shadows. |
| receives_shadows | `bool` | Whether this renderer receives shadows. |
| render_material | `Any` | The primary material used for rendering. |
| material_guid | `str` | The asset GUID of the primary material. |
| material_count | `int` | The number of material slots on this renderer. *(read-only)* |
| has_mesh_asset | `bool` | Whether a mesh asset is assigned to this renderer. *(read-only)* |
| mesh_asset_guid | `str` | The asset GUID of the assigned mesh. *(read-only)* |
| mesh_name | `str` | The name of the assigned mesh. *(read-only)* |
| vertex_count | `int` | The number of vertices in the mesh. *(read-only)* |
| index_count | `int` | The number of indices in the mesh. *(read-only)* |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Public Methods

| Method | Description |
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

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.resources import Material

class MeshSetup(InfComponent):
    def start(self):
        renderer = self.game_object.get_cpp_component("MeshRenderer")
        if not renderer:
            renderer = self.game_object.add_component("MeshRenderer")

        # Create and assign a lit material
        mat = Material.create_lit()
        mat.set_color("_BaseColor", 0.2, 0.6, 1.0, 1.0)
        renderer.render_material = mat

        # Configure shadow behavior
        renderer.casts_shadows = True
        renderer.receives_shadows = True

        # Inspect mesh data
        print(f"Vertices: {renderer.vertex_count}")
        print(f"Indices: {renderer.index_count}")
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Material](Material.md)
- [MeshData](MeshData.md)
- [Shader](Shader.md)
- [Transform](Transform.md)

<!-- USER CONTENT END -->
