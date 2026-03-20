# Debug

<div class="class-info">
类位于 <b>InfEngine.debug</b>
</div>

## 描述

调试工具类。

<!-- USER CONTENT START --> description

Debug 提供日志和可视化诊断工具。消息以不同严重级别显示在引擎控制台中：**Log**、**Warning** 和 **Error**。

使用 `Debug.log()` 输出一般信息，`Debug.log_warning()` 输出潜在问题，`Debug.log_error()` 输出需要注意的错误。`Debug.log_assert()` 可在开发期间验证条件。调用 `Debug.clear_console()` 清空控制台输出。

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `static Debug.log(message: Any, context: Any = ...) → None` | 输出日志消息到控制台。 |
| `static Debug.log_warning(message: Any, context: Any = ...) → None` | 输出警告消息到控制台。 |
| `static Debug.log_error(message: Any, context: Any = ..., source_file: str = ..., source_line: int = ...) → None` | 输出错误消息到控制台。 |
| `static Debug.log_exception(exception: Exception, context: Any = ...) → None` | Log an exception to the console. |
| `static Debug.log_assert(condition: bool, message: Any = ..., context: Any = ...) → None` | Assert a condition and log if it fails. |
| `static Debug.clear_console() → None` | Clear all messages in the debug console. |
| `static Debug.log_internal(message: Any, context: Any = ...) → None` | Log an internal engine message (hidden from user by default). |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.debug import Debug

class DebugExample(InfComponent):
    def start(self):
        Debug.log("游戏启动")
        Debug.log_warning("内存不足")
        Debug.log_error("着色器编译失败")

    def update(self):
        # 开发期间验证条件
        Debug.log_assert(self.game_object is not None, "缺少游戏对象")

        # 带上下文输出一次日志
        if self.time.frame_count == 1:
            Debug.log(f"第一帧间隔：{self.time.delta_time}", self)
```

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Gizmos](Gizmos.md) — 场景视图中的可视化调试
- [InfComponent](InfComponent.md) — 组件生命周期

<!-- USER CONTENT END -->
