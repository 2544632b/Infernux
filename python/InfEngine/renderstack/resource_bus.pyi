from __future__ import annotations

from typing import Dict, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from InfEngine.rendergraph.graph import TextureHandle


class ResourceBus:
    """Shared bus for passing texture handles between render passes."""

    def __init__(self, initial: Optional[Dict[str, TextureHandle]] = ...) -> None: ...
    def get(self, name: str) -> Optional[TextureHandle]:
        """Get a texture handle by resource name, or None."""
        ...
    def set(self, name: str, handle: TextureHandle) -> None:
        """Set a texture handle for a resource name."""
        ...
    def has(self, name: str) -> bool:
        """Check if a resource name is registered."""
        ...
    @property
    def available_resources(self) -> Set[str]:
        """Set of all registered resource names."""
        ...
    def snapshot(self) -> Dict[str, TextureHandle]:
        """Return a copy of the current resource state."""
        ...
    def __repr__(self) -> str: ...
