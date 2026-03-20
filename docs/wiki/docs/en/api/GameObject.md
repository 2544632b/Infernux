# GameObject

<div class="class-info">
class in <b>InfEngine</b>
</div>

## Description

A game object in the scene hierarchy with components.

<!-- USER CONTENT START --> description

GameObject is the fundamental building block of InfEngine scenes. Every entity in the game — characters, lights, cameras, props — is a GameObject. On its own, a GameObject is just a named container; it gains behavior entirely through the [Components](Component.md) attached to it.

Every GameObject automatically includes a [Transform](Transform.md) component that defines its position, rotation, and scale within the scene hierarchy. Attach additional components with `add_component()` to give the object visual appearance, physics, audio, or custom gameplay logic. Use `get_component()` and `get_py_component()` to retrieve components at runtime.

GameObjects form a parent-child hierarchy. Setting a parent with `set_parent()` makes the child's [Transform](Transform.md) relative to the parent, so moving the parent moves all its children. Use `find_child()` and `find_descendant()` to locate objects by name, and `compare_tag()` to identify objects by tag for gameplay logic such as collision filtering or target selection.

<!-- USER CONTENT END -->

## Properties

| Name | Type | Description |
|------|------|------|
| name | `str` | The name of this GameObject. |
| active | `bool` | Whether this GameObject is active. |
| id | `int` | Unique object ID. *(read-only)* |
| transform | `Transform` | Get the Transform component. *(read-only)* |
| active_self | `bool` | Is this object itself active? Alias for active. *(read-only)* |
| active_in_hierarchy | `bool` | Is this object active in the hierarchy? Unity: gameObject.activeInHierarchy *(read-only)* |
| is_static | `bool` | Static flag. |
| scene | `Optional[Scene]` | The Scene this GameObject belongs to. *(read-only)* |
| tag | `str` | Tag string for this GameObject. |
| layer | `int` | Layer index (0-31) for this GameObject. |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## Public Methods

| Method | Description |
|------|------|
| `get_transform() → Transform` | Get the Transform component. |
| `add_component(component_type: Union[str, type]) → Optional[Component]` | Add a C++ component by type or type name. |
| `remove_component(component: Component) → bool` | Remove a component instance (cannot remove Transform). |
| `get_components() → List[Component]` | Get all components (including Transform). |
| `get_cpp_component(type_name: str) → Optional[Component]` | Get a C++ component by type name (e.g., 'Transform', 'MeshRenderer', 'Light'). |
| `get_cpp_components(type_name: str) → List[Component]` | Get all C++ components of a given type name. |
| `add_py_component(component_instance: Any) → Optional[Any]` | Add a Python InfComponent instance to this GameObject. |
| `get_py_component(component_type: type) → Optional[Any]` | Get a Python component of the specified type. |
| `get_py_components() → List[Any]` | Get all Python components attached to this GameObject. |
| `remove_py_component(component: Any) → bool` | Remove a Python component instance. |
| `get_parent() → Optional[GameObject]` | Get the parent GameObject. |
| `set_parent(parent: Optional[GameObject], world_position_stays: bool = True) → None` | Set the parent GameObject (None for root). |
| `get_children() → List[GameObject]` | Get list of child GameObjects. |
| `get_child_count() → int` | Get the number of children. |
| `is_active_in_hierarchy() → bool` | Check if this object and all parents are active. |
| `get_child(index: int) → Optional[GameObject]` | Get child by index. |
| `find_child(name: str) → Optional[GameObject]` | Find direct child by name (non-recursive). |
| `find_descendant(name: str) → Optional[GameObject]` | Find descendant by name (recursive depth-first search). |
| `compare_tag(tag: str) → bool` | Returns True if this GameObject's tag matches the given tag. |
| `serialize() → str` | Serialize GameObject to JSON string. |
| `deserialize(json_str: str) → None` | Deserialize GameObject from JSON string. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent, serialized_field
from InfEngine.math import vector3

class PlayerSetup(InfComponent):
    speed: float = serialized_field(default=5.0)

    def start(self):
        # Rename the game object
        self.game_object.name = "Player"
        self.game_object.tag = "Player"

        # Add a mesh renderer for visual appearance
        renderer = self.game_object.add_component("MeshRenderer")

        # Create a child object for the weapon
        scene = self.game_object.scene
        weapon = scene.create_game_object("Sword")
        weapon.set_parent(self.game_object)
        weapon.transform.local_position = vector3(0.5, 0.0, 1.0)

    def update(self, delta_time: float):
        # Move the object forward each frame
        direction = self.transform.forward
        self.transform.translate(direction * self.speed * delta_time)

        # List all children
        for child in self.game_object.get_children():
            pass  # process each child
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Transform](Transform.md)
- [Component](Component.md)
- [InfComponent](InfComponent.md)
- [Scene](Scene.md)
- [SceneManager](SceneManager.md)

<!-- USER CONTENT END -->
