# disallow_multiple

<div class="class-info">
函数位于 <b>InfEngine.components</b>
</div>

```python
disallow_multiple() → Union[Type, Callable]
```

## 描述

Prevent multiple instances of this component on a GameObject.

Usable with or without parentheses::

    @disallow_multiple
    class MySingleton(InfComponent): ...

    @disallow_multiple()
    class MySingleton(InfComponent): ...

<!-- USER CONTENT START --> description

防止在同一 GameObject 上附加多个同类型组件实例。引擎会拒绝添加重复组件并输出警告。

等价于 Unity 的 `[DisallowMultipleComponent]` 特性。可以带或不带括号使用。

<!-- USER CONTENT END -->

## 示例

<!-- USER CONTENT START --> example

```python
from InfEngine import InfComponent
from InfEngine.components import disallow_multiple

@disallow_multiple
class GameManager(InfComponent):
    """每个 GameObject 只允许一个 GameManager。"""
    def start(self):
        Debug.log("GameManager 已初始化")
```

<!-- USER CONTENT END -->
