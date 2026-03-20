from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Set, TYPE_CHECKING

from InfEngine.renderstack.render_pass import RenderPass

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import RenderGraph
    from InfEngine.renderstack.resource_bus import ResourceBus


class FullScreenEffect(RenderPass):
    """Base class for fullscreen post-processing effects."""

    requires: ClassVar[Set[str]]
    modifies: ClassVar[Set[str]]
    menu_path: ClassVar[str]
    requires_per_frame_rebuild: ClassVar[bool]
    _serialized_fields_: ClassVar[Dict[str, Any]]

    def __init__(self, enabled: bool = ...) -> None: ...
    def setup_passes(self, graph: RenderGraph, bus: ResourceBus) -> None:
        """Override to add fullscreen passes to the render graph."""
        ...
    def get_shader_list(self) -> List[str]:
        """Return shader paths required by this effect."""
        ...
    def inject(self, graph: RenderGraph, bus: ResourceBus) -> None:
        """Inject this effect into the render graph."""
        ...
    def get_params_dict(self) -> Dict[str, Any]:
        """Get serializable parameters as a dictionary."""
        ...
    def set_params_dict(self, params: Dict[str, Any]) -> None:
        """Restore parameters from a dictionary."""
        ...
    def __repr__(self) -> str: ...
