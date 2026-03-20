from __future__ import annotations

from InfEngine.components.builtin_component import BuiltinComponent

class AudioListener(BuiltinComponent):
    """Represents the listener for 3D audio in the scene."""

    _cpp_type_name: str
    _component_category_: str

    # ---- Read-only properties ----

    @property
    def game_object_id(self) -> int:
        """The ID of the GameObject this component is attached to."""
        ...

    # ---- Serialization ----

    def serialize(self) -> str:
        """Serialize the component to a JSON string."""
        ...
    def deserialize(self, json_str: str) -> bool:
        """Deserialize the component from a JSON string."""
        ...
