"""Physics settings — load / save / apply project-level physics configuration.

Previously embedded in ``engine.ui.tag_layer_settings``; extracted here so
the physics subsystem owns its own configuration without depending on the
editor UI layer.
"""

from __future__ import annotations

import json
import os
from typing import Dict

from InfEngine.math.coerce import coerce_vec3

_PHYSICS_SETTINGS_FILE = "PhysicsSettings.json"

DEFAULT_PHYSICS_SETTINGS: Dict[str, object] = {
    "gravity": [0.0, -9.81, 0.0],
    "fixed_delta_time": 0.02,
    "max_fixed_delta_time": 0.1,
}


def settings_path(project_path: str) -> str:
    """Return the absolute path to the physics settings JSON file."""
    return os.path.join(project_path, "ProjectSettings", _PHYSICS_SETTINGS_FILE)


def load(project_path: str) -> dict:
    """Load physics settings from *project_path*, falling back to defaults."""
    if not project_path:
        return dict(DEFAULT_PHYSICS_SETTINGS)

    path = settings_path(project_path)
    if not os.path.isfile(path):
        return dict(DEFAULT_PHYSICS_SETTINGS)

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError, ValueError):
        return dict(DEFAULT_PHYSICS_SETTINGS)

    result = dict(DEFAULT_PHYSICS_SETTINGS)
    gravity = data.get("gravity")
    if isinstance(gravity, list) and len(gravity) >= 3:
        result["gravity"] = [float(gravity[0]), float(gravity[1]), float(gravity[2])]
    if "fixed_delta_time" in data:
        result["fixed_delta_time"] = max(0.001, float(data["fixed_delta_time"]))
    if "max_fixed_delta_time" in data:
        result["max_fixed_delta_time"] = max(result["fixed_delta_time"], float(data["max_fixed_delta_time"]))
    return result


def save(project_path: str, settings: dict) -> None:
    """Persist physics settings to *project_path*."""
    if not project_path:
        return
    path = settings_path(project_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def apply(settings: dict) -> None:
    """Push *settings* into the live engine (gravity, fixed timestep, etc.)."""
    from InfEngine.lib import SceneManager, Vector3
    from InfEngine.physics import Physics
    from InfEngine.timing import Time

    gravity = settings.get("gravity", DEFAULT_PHYSICS_SETTINGS["gravity"])
    fixed_dt = max(0.001, float(settings.get("fixed_delta_time", DEFAULT_PHYSICS_SETTINGS["fixed_delta_time"])))
    max_fixed_dt = max(fixed_dt, float(settings.get("max_fixed_delta_time", DEFAULT_PHYSICS_SETTINGS["max_fixed_delta_time"])))

    Physics.gravity = coerce_vec3(gravity)
    sm = SceneManager.instance()
    sm.set_fixed_time_step(fixed_dt)
    sm.set_max_fixed_delta_time(max_fixed_dt)
    Time.fixed_delta_time = fixed_dt
