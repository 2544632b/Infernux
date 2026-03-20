# LayerMask

<div class="class-info">
类位于 <b>InfEngine.scene</b>
</div>

## 描述

Utility for working with layer-based filtering.

<!-- USER CONTENT START --> description

LayerMask 是创建选择特定层的位掩码的工具。层被[摄像机](Camera.md)用于剔除、物理查询用于过滤以及渲染用于选择性可见。

<!-- USER CONTENT END -->

## 静态方法

| 方法 | 描述 |
|------|------|
| `static LayerMask.get_mask() → int` | Get a layer mask from one or more layer names. |
| `static LayerMask.layer_to_name(layer: int) → str` | Get the name of a layer by its index. |
| `static LayerMask.name_to_layer(name: str) → int` | Get the index of a layer by its name. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## 示例

```python
# TODO: Add example for LayerMask
```

<!-- USER CONTENT START --> example

<!-- USER CONTENT END -->

## 另请参阅

<!-- USER CONTENT START --> see_also

- [Camera](Camera.md)
- [GameObject](GameObject.md)

<!-- USER CONTENT END -->
