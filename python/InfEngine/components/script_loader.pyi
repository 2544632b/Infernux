"""Type stubs for InfEngine.components.script_loader."""

from __future__ import annotations

from typing import Dict, List, Optional, Type

from .component import InfComponent


class ScriptLoadError(Exception):
    """Raised when a script cannot be loaded or contains no valid components."""
    ...


def set_script_error(file_path: str, message: str) -> None:
    """Record an error message for a script (no exception object needed)."""
    ...

def get_script_errors() -> Dict[str, str]:
    """Return a snapshot of all currently broken scripts {path: traceback}."""
    ...

def has_script_errors() -> bool:
    """Return True if any loaded script has unresolved errors."""
    ...

def get_script_error_by_path(file_path: str) -> Optional[str]:
    """Return the error string for *file_path*, or ``None`` if it loaded OK."""
    ...


def load_component_from_file(file_path: str) -> Type[InfComponent]:
    """Load the first InfComponent subclass from a Python file.

    Raises:
        ScriptLoadError: If file doesn't exist, can't be imported,
                         or contains no components.
    """
    ...


def load_all_components_from_file(file_path: str) -> List[Type[InfComponent]]:
    """Load all InfComponent subclasses from a Python file.

    Raises:
        ScriptLoadError: If file doesn't exist or can't be imported.
    """
    ...


def create_component_instance(component_class: Type[InfComponent]) -> InfComponent:
    """Create an instance of a component class.

    Raises:
        ScriptLoadError: If instantiation fails.
    """
    ...


def load_and_create_component(
    file_path: str, asset_database: Optional[object] = ...
) -> Optional[InfComponent]:
    """Load first component from file and create an instance.

    Returns ``None`` if the script has errors (already logged).

    Raises:
        ScriptLoadError: If AssetDatabase is missing or GUID cannot be resolved.
    """
    ...


def get_component_info(component_class: Type[InfComponent]) -> dict:
    """Extract metadata from a component class.

    Returns:
        Dict with keys ``name``, ``module``, ``docstring``, ``fields``.
    """
    ...
