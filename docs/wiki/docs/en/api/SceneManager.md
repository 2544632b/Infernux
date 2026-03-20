# SceneManager

<div class="class-info">
class in <b>InfEngine.scene</b>
</div>

## Description

Manages scene loading, unloading, and queries.

<!-- USER CONTENT START --> description

SceneManager provides static methods for loading, unloading, and querying scenes at runtime. It is the central point for scene lifecycle management in InfEngine.

Use `get_active_scene()` to obtain the currently active [Scene](Scene.md). Call `load_scene()` to load a scene by file path, and `get_scene_count()` or `get_scene_at()` to enumerate loaded scenes. Scene loading replaces the current scene hierarchy, so save any persistent data before switching.

SceneManager is a static utility class — you never instantiate it. All methods are called directly on the class, such as `SceneManager.get_active_scene()`.

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `static SceneManager.get_active_scene() → Optional[object]` | Get the currently active scene. |
| `static SceneManager.get_scene_by_name(name: str) → Optional[str]` | Get a scene path by its name. |
| `static SceneManager.get_scene_by_build_index(build_index: int) → Optional[str]` | Get a scene path by its build index. |
| `static SceneManager.get_scene_at(index: int) → Optional[str]` | Get a scene path by its index in the scene list. |
| `static SceneManager.load_scene(scene: Union[int, str]) → bool` | Load a scene by file path or build index. |
| `static SceneManager.process_pending_load() → None` | Process any pending scene load request. |
| `static SceneManager.get_scene_count() → int` | Get the total number of scenes in the build. |
| `static SceneManager.get_scene_name(build_index: int) → Optional[str]` | Get a scene name by build index. |
| `static SceneManager.get_scene_path(build_index: int) → Optional[str]` | Get a scene file path by build index. |
| `static SceneManager.get_build_index(name: str) → int` | Get the build index of a scene by name. |
| `static SceneManager.get_all_scene_names() → List[str]` | Get a list of all scene names in the build. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Example

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent, SceneManager

class LevelLoader(InfComponent):
    def start(self):
        # Get the active scene
        active = SceneManager.get_active_scene()
        print(f"Current scene: {active.name}")

        # Check how many scenes are loaded
        count = SceneManager.get_scene_count()
        for i in range(count):
            scene = SceneManager.get_scene_at(i)
            print(f"Scene {i}: {scene.name}")

    def load_next_level(self):
        # Load a new scene by path
        SceneManager.load_scene("scenes/level_02.scene")
```

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Scene](Scene.md)
- [GameObject](GameObject.md)

<!-- USER CONTENT END -->
