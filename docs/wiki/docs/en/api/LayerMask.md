# LayerMask

<div class="class-info">
class in <b>InfEngine.scene</b>
</div>

## Description

Utility for working with layer-based filtering.

<!-- USER CONTENT START --> description

LayerMask is a utility for creating bitmasks that select specific layers. Layers are used by [Cameras](Camera.md) for culling, physics queries for filtering, and rendering for selective visibility.

<!-- USER CONTENT END -->

## Static Methods

| Method | Description |
|------|------|
| `static LayerMask.get_mask() → int` | Get a layer mask from one or more layer names. |
| `static LayerMask.layer_to_name(layer: int) → str` | Get the name of a layer by its index. |
| `static LayerMask.name_to_layer(name: str) → int` | Get the index of a layer by its name. |

<!-- USER CONTENT START --> static_methods

<!-- USER CONTENT END -->

## Example

```python
# TODO: Add example for LayerMask
```

<!-- USER CONTENT START --> example

<!-- USER CONTENT END -->

## See Also

<!-- USER CONTENT START --> see_also

- [Camera](Camera.md)
- [GameObject](GameObject.md)

<!-- USER CONTENT END -->
