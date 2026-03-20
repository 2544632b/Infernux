# ── Runtime API (used by game scripts) ─────────────────────────────
from InfEngine.engine import release_engine, Engine, LogLevel
from InfEngine.math import Vector2, Vector3, vec4f, quatf, vector2, vector3, vector4, quaternion
from InfEngine.components import InfComponent, serialized_field
from InfEngine.components import GameObjectRef, MaterialRef
from InfEngine.components import BuiltinComponent, CppProperty, Light, MeshRenderer, Camera
from InfEngine.components import AudioSource, AudioListener
from InfEngine.lib import Space
from InfEngine.debug import Debug, debug, log, log_warning, log_error, log_exception
from InfEngine import core
from InfEngine import rendergraph
from InfEngine import renderstack
from InfEngine import scene
from InfEngine import input
from InfEngine import ui
from InfEngine.timing import Time
from InfEngine.mathf import Mathf
from InfEngine.coroutine import (
    Coroutine,
    WaitForSeconds,
    WaitForSecondsRealtime,
    WaitForEndOfFrame,
    WaitForFixedUpdate,
    WaitUntil,
    WaitWhile,
)