# SceneManager

<div class="class-info">
类位于 <b>InfEngine.scene</b>
</div>

## 描述

运行时场景加载与卸载管理器。

<!-- USER CONTENT START --> description

SceneManager 提供用于在运行时加载、卸载和查询场景的静态方法，是 InfEngine 中场景生命周期管理的核心。

使用 `get_active_scene()` 获取当前活动的 [Scene](Scene.md)。调用 `load_scene()` 根据文件路径加载场景，使用 `get_scene_count()` 或 `get_scene_at()` 枚举已加载的场景。加载新场景会替换当前场景层级，因此在切换前应保存所有需要持久化的数据。

SceneManager 是一个静态工具类——无需实例化。所有方法直接在类上调用，例如 `SceneManager.get_active_scene()`。

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `static SceneManager.get_active_scene() → Optional[object]` | 获取当前活动场景。 |
| `static SceneManager.get_scene_by_name(name: str) → Optional[str]` | Get a scene path by its name. |
| `static SceneManager.get_scene_by_build_index(build_index: int) → Optional[str]` | Get a scene path by its build index. |
| `static SceneManager.get_scene_at(index: int) → Optional[str]` | 按索引获取已加载的场景。 |
| `static SceneManager.load_scene(scene: Union[int, str]) → bool` | 按名称或路径加载场景。 |
| `static SceneManager.process_pending_load() → None` | Process any pending scene load request. |
| `static SceneManager.get_scene_count() → int` | 获取已加载的场景数量。 |
| `static SceneManager.get_scene_name(build_index: int) → Optional[str]` | Get a scene name by build index. |
| `static SceneManager.get_scene_path(build_index: int) → Optional[str]` | Get a scene file path by build index. |
| `static SceneManager.get_build_index(name: str) → int` | Get the build index of a scene by name. |
| `static SceneManager.get_all_scene_names() → List[str]` | Get a list of all scene names in the build. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent, SceneManager

class LevelLoader(InfComponent):
    def start(self):
        # 获取当前活动场景
        active = SceneManager.get_active_scene()
        print(f"当前场景：{active.name}")

        # 检查已加载的场景数量
        count = SceneManager.get_scene_count()
        for i in range(count):
            scene = SceneManager.get_scene_at(i)
            print(f"场景 {i}：{scene.name}")

    def load_next_level(self):
        # 根据路径加载新场景
        SceneManager.load_scene("scenes/level_02.scene")
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Scene 场景](Scene.md)
- [GameObject](GameObject.md)

<!-- USER CONTENT END -->
