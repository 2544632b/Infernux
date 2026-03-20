from __future__ import annotations

from InfEngine.components.builtin.collider import Collider

class MeshCollider(Collider):
    """A collider that uses a mesh shape."""

    _cpp_type_name: str

    # ---- CppProperty fields as properties ----

    @property
    def convex(self) -> bool:
        """Whether the mesh collider uses a convex hull."""
        ...
    @convex.setter
    def convex(self, value: bool) -> None: ...

    # ---- Gizmos ----

    def on_draw_gizmos_selected(self) -> None:
        """Draw the collider wireframe when selected in the editor."""
        ...
