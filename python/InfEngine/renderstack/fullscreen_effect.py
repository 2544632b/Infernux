"""
FullScreenEffect — Multi-pass fullscreen post-processing effect base class.

A FullScreenEffect is a higher-level abstraction above ``RenderPass`` that
represents a **complete, parameterised, multi-pass fullscreen effect** such
as Bloom, Vignette, or SSAO.

Subclass hierarchy::

    RenderPass
    └── FullScreenEffect          (this module)
        ├── BloomEffect           (built-in)
        └── ...user-defined...

Subclass contract:
    1. Define ``name``, ``injection_point``, ``default_order``
    2. Declare tuneable parameters via ``serialized_field``
    3. Implement ``setup_passes(graph, bus)`` — inject all passes into the graph
    4. Optionally implement ``get_shader_list()`` for validation / precompilation

Integration with RenderStack:
    FullScreenEffect inherits RenderPass, so it is transparently discovered,
    mounted, validated, and serialised by the existing RenderStack machinery.
    ``inject()`` delegates to ``setup_passes()`` — subclasses override
    ``setup_passes`` instead of ``inject``.

Parameter serialization:
    Uses the same ``serialized_field`` / ``__init_subclass__`` mechanism as
    ``RenderPipeline``.  Parameters are persisted in the scene JSON via
    ``RenderStack.on_before_serialize()`` and restored by
    ``on_after_deserialize()``.
"""

from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Set, TYPE_CHECKING

from InfEngine.renderstack.render_pass import RenderPass
from InfEngine.renderstack._serialized_field_mixin import SerializedFieldCollectorMixin

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import RenderGraph
    from InfEngine.rendergraph.graph import Format
    from InfEngine.renderstack.resource_bus import ResourceBus


class FullScreenEffect(SerializedFieldCollectorMixin, RenderPass):
    """多 pass 全屏后处理效果基类。

    子类必须定义:
        - ``name``: 全局唯一的效果名称
        - ``injection_point``: 目标注入点（如 ``"before_post_process"``）
        - ``default_order``: 同注入点内排序值

    子类可选定义:
        - ``menu_path``: 编辑器菜单中的分类路径（如 ``"Post-processing/Bloom"``）

    子类通过 ``serialized_field`` 声明可调参数::

        class BloomEffect(FullScreenEffect):
            menu_path = "Post-processing/Bloom"
            threshold: float = serialized_field(default=1.0, range=(0, 10))
            intensity: float = serialized_field(default=0.5, range=(0, 3))

    子类实现 ``setup_passes(graph, bus)`` 向 graph 注入所有渲染 pass。
    """

    # ---- 默认资源声明（大多数全屏效果读 + 改 color） ----
    requires: ClassVar[Set[str]] = {"color"}
    modifies: ClassVar[Set[str]] = {"color"}

    # ---- 编辑器分类路径（可选） ----
    menu_path: ClassVar[str] = ""

    # ---- Reserved attrs for the mixin ----
    _reserved_attrs_ = frozenset({
        "name", "injection_point", "default_order", "menu_path",
        "requires", "modifies", "creates", "enabled",
    })

    # ---- 类级序列化字段元数据 ----
    _serialized_fields_: ClassVar[Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Instance init
    # ------------------------------------------------------------------

    def __init__(self, enabled: bool = True) -> None:
        super().__init__(enabled=enabled)
        # Prime instance storage for serialized fields
        from InfEngine.components.serialized_field import get_serialized_fields
        for field_name, meta in get_serialized_fields(self.__class__).items():
            if not hasattr(self, f"_sf_{field_name}"):
                try:
                    setattr(self, field_name, meta.default)
                except (AttributeError, TypeError):
                    pass

    # ==================================================================
    # Texture helper — eliminates per-effect _tex() boilerplate
    # ==================================================================

    @staticmethod
    def get_or_create_texture(
        graph: "RenderGraph",
        name: str,
        *,
        format: "Format" = None,
        camera_target: bool = False,
        size=None,
        size_divisor: int = 0,
    ):
        """Return an existing texture from *graph*, or create a new one.

        The ``*`` makes the configuration arguments keyword-only, so call
        sites stay readable::

            _tex(graph, "_bloom_mip0", format=Format.RGBA16_SFLOAT, size_divisor=2)

        Args:
            graph: Render graph that owns the texture resource.
            name: Graph-local texture alias.
            format: Texture format. ``None`` uses ``RenderGraph.create_texture``
                default format.
            camera_target: Whether this texture is the camera's main color
                target.
            size: Explicit texture size ``(width, height)``.
            size_divisor: Resolution scale divisor relative to the scene size.
        """
        existing = graph.get_texture(name)
        if existing is not None:
            return existing

        create_kwargs = {
            "camera_target": camera_target,
            "size": size,
            "size_divisor": size_divisor,
        }
        if format is not None:
            create_kwargs["format"] = format

        return graph.create_texture(name, **create_kwargs)

    # ==================================================================
    # Core interface — subclasses implement these
    # ==================================================================

    def setup_passes(self, graph: "RenderGraph", bus: "ResourceBus") -> None:
        """向 RenderGraph 注入本效果的所有渲染 pass。

        子类实现此方法:
        1. 从 bus 获取输入资源（如 ``bus.get("color")``）
        2. 创建中间纹理（如 ``graph.create_texture(...)``）
        3. 按顺序添加 pass，指定 shader 和操作
        4. 将修改后的资源写回 bus

        Args:
            graph: 当前构建中的 RenderGraph。
            bus: 资源总线。
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement setup_passes()"
        )

    def get_shader_list(self) -> List[str]:
        """返回本效果使用的所有 shader id 列表。

        用于:
        - Editor 预验证 shader 是否存在
        - 未来的 shader 预编译 / 缓存

        Returns:
            shader id 列表，如 ``["bloom_prefilter", "bloom_downsample", ...]``
        """
        return []

    # ==================================================================
    # inject() — bridge to RenderStack
    # ==================================================================

    def inject(self, graph: "RenderGraph", bus: "ResourceBus") -> None:
        """由 RenderStack 调用。委托到 ``setup_passes()``。

        子类不应重写此方法——重写 ``setup_passes()`` 即可。
        """
        if not self.enabled:
            return
        self.setup_passes(graph, bus)

    # ==================================================================
    # Serialization helpers
    # ==================================================================

    def get_params_dict(self) -> Dict[str, Any]:
        """导出当前参数为可 JSON 序列化的字典。"""
        from InfEngine.components.serialized_field import get_serialized_fields
        from enum import Enum

        params: Dict[str, Any] = {}
        for field_name in get_serialized_fields(self.__class__):
            value = getattr(self, field_name, None)
            if isinstance(value, Enum):
                params[field_name] = {"__enum_name__": value.name}
            else:
                params[field_name] = value
        return params

    def set_params_dict(self, params: Dict[str, Any]) -> None:
        """从字典恢复参数。"""
        from InfEngine.components.serialized_field import get_serialized_fields, FieldType

        fields = get_serialized_fields(self.__class__)
        self._inf_deserializing = True
        try:
            for field_name, value in params.items():
                meta = fields.get(field_name)
                if meta is None:
                    continue
                try:
                    if (meta.field_type == FieldType.ENUM
                            and isinstance(value, dict)
                            and "__enum_name__" in value):
                        enum_cls = meta.enum_type
                        enum_name = value["__enum_name__"]
                        if enum_cls is not None and enum_name in enum_cls.__members__:
                            setattr(self, field_name, enum_cls[enum_name])
                            continue
                    setattr(self, field_name, value)
                except (AttributeError, TypeError, ValueError):
                    continue
        finally:
            self._inf_deserializing = False

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} name='{self.name}' "
            f"point='{self.injection_point}' "
            f"enabled={self.enabled}>"
        )
