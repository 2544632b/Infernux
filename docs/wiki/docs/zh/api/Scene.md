# Scene

<div class="class-info">
类位于 <b>InfEngine</b>
</div>

## 描述

运行时场景，包含 GameObject 层级。

<!-- USER CONTENT START --> description

Scene 代表引擎中的一个运行时场景，包含 [GameObject](GameObject.md) 的层级结构。每个对象都存在于某个场景中，场景提供创建、查找和枚举对象的方法。

使用 `create_game_object()` 在场景中实例化新对象，使用 `find()` 根据名称定位对象，使用 `find_with_tag()` 根据标签搜索。`get_root_game_objects()` 方法仅返回顶层对象（即没有父级的对象），适合遍历整个层级结构。

场景的加载和卸载通过 [SceneManager](SceneManager.md) 完成。当前活动场景决定了新创建对象的默认放置位置。

<!-- USER CONTENT END -->

## 属性

| 名称 | 类型 | 描述 |
|------|------|------|
| name | `str` | 场景名称。 |

<!-- USER CONTENT START --> properties

<!-- USER CONTENT END -->

## 公共方法

| 方法 | 描述 |
|------|------|
| `create_game_object(name: str = 'GameObject') → GameObject` | Create a new empty GameObject in this scene. |
| `create_primitive(type: PrimitiveType, name: str = '') → GameObject` | Create a primitive GameObject (Cube, Sphere, Capsule, Cylinder, Plane). |
| `get_root_objects() → List[GameObject]` | Get all root-level GameObjects. |
| `get_all_objects() → List[GameObject]` | Get all GameObjects in the scene. |
| `find(name: str) → Optional[GameObject]` | Find a GameObject by name. |
| `find_by_id(id: int) → Optional[GameObject]` | Find a GameObject by ID. |
| `find_with_tag(tag: str) → Optional[GameObject]` | Find the first GameObject with a given tag. |
| `find_game_objects_with_tag(tag: str) → List[GameObject]` | Find all GameObjects with a given tag. |
| `find_game_objects_in_layer(layer: int) → List[GameObject]` | Find all GameObjects in a given layer. |
| `destroy_game_object(game_object: GameObject) → None` | Destroy a GameObject (removed at end of frame). |
| `process_pending_destroys() → None` | Process pending GameObject destroys. |
| `is_playing() → bool` | Check if the scene is in play mode. |
| `serialize() → str` | Serialize scene to JSON string. |
| `deserialize(json_str: str) → None` | Deserialize scene from JSON string. |
| `save_to_file(path: str) → None` | Save scene to a JSON file. |
| `load_from_file(path: str) → None` | Load scene from a JSON file. |
| `has_pending_py_components() → bool` | Check if there are pending Python components to restore. |
| `take_pending_py_components() → List[PendingPyComponent]` | Get and clear pending Python components for restoration. |

<!-- USER CONTENT START --> public_methods

<!-- USER CONTENT END -->

## 生命周期方法

| 方法 | 描述 |
|------|------|
| `start() → None` | Trigger Awake+Start on all components (idempotent — skipped if already started). |

<!-- USER CONTENT START --> lifecycle_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.math import vector3

class SceneSetup(InfComponent):
    def start(self):
        scene = self.game_object.scene

        # 在场景中创建新对象
        ground = scene.create_game_object("Ground")
        ground.transform.position = vector3(0, -0.5, 0)

        # 根据名称查找已有对象
        player = scene.find("Player")
        if player:
            print(f"已找到：{player.name}")

        # 根据标签查找对象
        enemy = scene.find_with_tag("Enemy")

        # 遍历所有根级对象
        roots = scene.get_root_game_objects()
        for obj in roots:
            print(f"根对象：{obj.name}")
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [SceneManager 场景管理器](SceneManager.md)
- [GameObject](GameObject.md)
- [Transform](Transform.md)

<!-- USER CONTENT END -->
