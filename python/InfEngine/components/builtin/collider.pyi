from __future__ import annotations

from typing import Any

from InfEngine.components.builtin_component import BuiltinComponent

class Collider(BuiltinComponent):
    """Base class for all collider components."""

    _cpp_type_name: str
    _component_category_: str
    _always_show: bool

    # ---- CppProperty fields as properties ----

    @property
    def center(self) -> Any:
        """The center of the collider in local space."""
        ...
    @center.setter
    def center(self, value: Any) -> None: ...

    @property
    def is_trigger(self) -> bool:
        """Whether the collider is a trigger (non-physical)."""
        ...
    @is_trigger.setter
    def is_trigger(self, value: bool) -> None: ...

    @property
    def friction(self) -> float:
        """The friction coefficient of the collider surface."""
        ...
    @friction.setter
    def friction(self, value: float) -> None: ...

    @property
    def bounciness(self) -> float:
        """The bounciness of the collider surface."""
        ...
    @bounciness.setter
    def bounciness(self, value: float) -> None: ...
