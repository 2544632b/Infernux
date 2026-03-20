# InfEngine Wiki

Welcome to the InfEngine documentation wiki.

## Quick Links

- [API Reference (English)](en/api/index.md)
- [API 参考手册 (中文)](zh/api/index.md)

## Getting Started

InfEngine is an open-source game engine with a C++17/Vulkan backend and Python scripting frontend. Write game logic in Python while the engine handles high-performance rendering, physics, and audio.

### Hello World

```python
from InfEngine import *

class HelloWorld(InfComponent):
    speed: float = serialized_field(default=5.0)
    
    def start(self):
        Debug.log("Hello, InfEngine!")
    
    def update(self):
        self.transform.rotate(vector3(0, self.speed * Time.delta_time, 0))
```

## Modules

| Module | Description |
|--------|-------------|
| [InfEngine](en/api/index.md) | Core types — GameObject, Transform, Scene, Component |
| [InfEngine.components](en/api/InfComponent.md) | Component system — InfComponent, serialized_field, decorators |
| [InfEngine.core](en/api/Material.md) | Assets — Material, Texture, Shader, MeshData |
| [InfEngine.input](en/api/Input.md) | Input system — keyboard, mouse, touch |
| [InfEngine.math](en/api/vector3.md) | Math — vector2, vector3, vector4 |
| [InfEngine.scene](en/api/SceneManager.md) | Scene management |
| [InfEngine.debug](en/api/Debug.md) | Logging and diagnostics |
| [InfEngine.gizmos](en/api/Gizmos.md) | Visual debugging aids |
