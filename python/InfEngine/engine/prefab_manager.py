"""
Prefab system for InfEngine.

Handles saving GameObjects as .prefab files and instantiating them back into scenes.
Prefab files contain the serialized JSON from GameObject.serialize(), wrapped in an
envelope with a prefab_version field.
"""

import json
import os

from InfEngine.debug import Debug

PREFAB_EXTENSION = ".prefab"
PREFAB_VERSION = 1


def save_prefab(game_object, file_path: str, asset_database=None) -> bool:
    """Serialize a GameObject hierarchy to a .prefab file.

    Returns True on success, False on failure.
    """
    if game_object is None:
        Debug.log_warning("Cannot save prefab: no GameObject provided.")
        return False

    if not file_path.lower().endswith(PREFAB_EXTENSION):
        file_path += PREFAB_EXTENSION

    try:
        go_json_str = game_object.serialize()
        go_data = json.loads(go_json_str)
    except Exception as exc:
        Debug.log_error(f"Failed to serialize GameObject for prefab: {exc}")
        return False

    # Strip any existing prefab linkage from the saved template
    _strip_prefab_fields(go_data)

    prefab_data = {
        "prefab_version": PREFAB_VERSION,
        "root_object": go_data,
    }

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(prefab_data, f, indent=2, ensure_ascii=False)
    except OSError as exc:
        Debug.log_error(f"Failed to write prefab file: {exc}")
        return False

    if asset_database:
        try:
            guid = asset_database.import_asset(file_path)
            Debug.log_internal(f"Registered prefab: {os.path.basename(file_path)} -> {guid}")
        except Exception as exc:
            Debug.log_warning(f"Failed to register prefab in AssetDatabase: {exc}")

    Debug.log_internal(f"Prefab saved: {file_path}")
    return True


def instantiate_prefab(file_path: str = None, guid: str = None,
                       scene=None, parent=None, asset_database=None):
    """Instantiate a prefab into the active scene.

    Supply either *file_path* or *guid* (GUID is resolved via asset_database).
    Returns the root GameObject, or None on failure.
    """
    # Resolve path from GUID if needed
    resolved_guid = guid or ""
    if not file_path and guid and asset_database:
        file_path = asset_database.get_path_from_guid(guid)

    if not file_path or not os.path.isfile(file_path):
        Debug.log_warning(f"Prefab file not found: {file_path}")
        return None

    # If we have a path but no GUID, try to resolve GUID from the asset database
    if not resolved_guid and asset_database:
        try:
            resolved_guid = asset_database.get_guid_from_path(file_path) or ""
        except Exception:
            resolved_guid = ""

    if scene is None:
        from InfEngine.lib import SceneManager
        scene = SceneManager.instance().get_active_scene()
    if scene is None:
        Debug.log_warning("No active scene — cannot instantiate prefab.")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            prefab_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        Debug.log_error(f"Failed to read prefab file: {exc}")
        return None

    root_obj_data = prefab_data.get("root_object")
    if root_obj_data is None:
        Debug.log_error("Invalid prefab file: missing 'root_object'.")
        return None

    # Stamp prefab linkage into the JSON before instantiation
    if resolved_guid:
        _stamp_prefab_guid(root_obj_data, resolved_guid)

    # Use C++ InstantiateFromJson — creates fresh IDs and collects pending py_components
    go_json_str = json.dumps(root_obj_data)
    new_obj = scene.instantiate_from_json(go_json_str, parent)
    if new_obj is None:
        Debug.log_error("Failed to instantiate prefab from JSON.")
        return None

    # Restore Python components that were collected as pending
    _restore_pending_py_components(scene, asset_database)

    return new_obj


def _stamp_prefab_guid(obj_data: dict, guid: str, is_root: bool = True):
    """Recursively stamp prefab_guid (and prefab_root on root) into JSON data."""
    obj_data["prefab_guid"] = guid
    if is_root:
        obj_data["prefab_root"] = True
    for child in obj_data.get("children", []):
        _stamp_prefab_guid(child, guid, is_root=False)


def _strip_prefab_fields(obj_data: dict):
    """Recursively remove prefab_guid/prefab_root so the template is clean."""
    obj_data.pop("prefab_guid", None)
    obj_data.pop("prefab_root", None)
    for child in obj_data.get("children", []):
        _strip_prefab_fields(child)


def _restore_pending_py_components(scene, asset_database=None):
    """Restore any pending Python components after prefab instantiation."""
    if not scene.has_pending_py_components():
        return

    pending = scene.take_pending_py_components()
    if not pending:
        return

    from InfEngine.engine.scene_manager import SceneFileManager
    sfm = SceneFileManager.instance()
    if sfm is None:
        # Fallback: do inline restoration
        _restore_pending_inline(scene, pending, asset_database)
        return

    # Use SceneFileManager's restoration logic
    for pc in pending:
        try:
            sfm._restore_single_py_component(scene, pc)
        except Exception as exc:
            Debug.log_error(
                f"Failed to restore component '{pc.type_name}' on "
                f"GameObject {pc.game_object_id}: {exc}"
            )


def _restore_pending_inline(scene, pending, asset_database):
    """Minimal inline restoration when SceneFileManager is not available."""
    for pc in pending:
        try:
            go = scene.find_by_id(pc.game_object_id)
            if not go:
                continue

            script_path = None
            if pc.script_guid and asset_database:
                script_path = asset_database.get_path_from_guid(pc.script_guid)

            # In packaged builds .py sources are compiled to .pyc and removed.
            if script_path and not os.path.exists(script_path) and script_path.endswith('.py'):
                pyc = script_path + 'c'
                if os.path.exists(pyc):
                    script_path = pyc

            # Packaged-build fallback: use build-time GUID manifest
            if not script_path and pc.script_guid:
                from InfEngine.engine.project_context import resolve_guid_to_path
                script_path = resolve_guid_to_path(pc.script_guid)

            instance = None
            if script_path:
                from InfEngine.components.script_loader import load_and_create_component
                instance = load_and_create_component(script_path, asset_database=asset_database)
            else:
                from InfEngine.components.registry import get_type
                comp_class = get_type(pc.type_name)
                if comp_class:
                    instance = comp_class()

            if instance is None:
                continue

            # Deserialize fields
            if pc.fields_json:
                import json as _json
                fields = _json.loads(pc.fields_json)
                from InfEngine.components.component import InfComponent
                if isinstance(instance, InfComponent):
                    instance._deserialize_fields(fields)

            instance.enabled = pc.enabled
            go.add_py_component(instance)
        except Exception as exc:
            Debug.log_error(
                f"Inline restore failed for '{pc.type_name}': {exc}"
            )
