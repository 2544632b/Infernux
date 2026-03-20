from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from InfEngine.components.component import InfComponent
from InfEngine.renderstack.injection_point import InjectionPoint
from InfEngine.renderstack.resource_bus import ResourceBus

if TYPE_CHECKING:
    from InfEngine.renderstack.render_pass import RenderPass
    from InfEngine.rendering.render_pipeline import RenderPipeline


@dataclass
class PassEntry:
    """Entry associating a render pass with its enabled state and order."""

    render_pass: RenderPass
    enabled: bool = ...
    order: int = ...


class RenderStack(InfComponent):
    """Component that manages a stack of render passes driven by a pipeline."""

    pipeline_class_name: str
    mounted_passes_json: str
    pipeline_params_json: str

    def awake(self) -> None:
        """Initialize the render stack on component awake."""
        ...
    def on_destroy(self) -> None:
        """Clean up the render stack when the component is destroyed."""
        ...

    @staticmethod
    def discover_pipelines() -> Dict[str, type]:
        """Discover all available render pipeline classes."""
        ...
    def set_pipeline(self, pipeline_class_name: str) -> None:
        """Set the active render pipeline by class name."""
        ...

    @property
    def pipeline(self) -> RenderPipeline:
        """The currently active render pipeline."""
        ...
    @property
    def injection_points(self) -> List[InjectionPoint]:
        """List of injection points defined by the pipeline."""
        ...
    @property
    def pass_entries(self) -> List[PassEntry]:
        """All mounted render pass entries."""
        ...

    def add_pass(self, render_pass: RenderPass) -> bool:
        """Add a render pass to the stack. Returns True on success."""
        ...
    def remove_pass(self, pass_name: str) -> bool:
        """Remove a render pass by name. Returns True if found."""
        ...
    def set_pass_enabled(self, pass_name: str, enabled: bool) -> None:
        """Enable or disable a render pass by name."""
        ...
    def reorder_pass(self, pass_name: str, new_order: int) -> None:
        """Change the execution order of a render pass."""
        ...
    def move_pass_before(self, dragged_name: str, target_name: str) -> None:
        """Move a render pass to execute before another pass."""
        ...
    def get_passes_at(self, injection_point: str) -> List[PassEntry]:
        """Get all pass entries at a specific injection point."""
        ...

    def invalidate_graph(self) -> None:
        """Mark the render graph as dirty, triggering a rebuild."""
        ...
    def build_graph(self) -> Any:
        """Build and return the render graph description."""
        ...
    def render(self, context: Any, camera: Any) -> None:
        """Execute the render stack for a camera."""
        ...


__all__ = [
    "PassEntry",
    "RenderStack",
]
