import os

# ── Player mode detection ───────────────────────────────────────────
# Set by the Nuitka boot script BEFORE any InfEngine imports.
# Guards editor-only imports to keep standalone builds fast and lean.
_PLAYER_MODE = os.environ.get("_INFENGINE_PLAYER_MODE")

from InfEngine.lib import InfGUIRenderable, InfGUIContext, TextureLoader, TextureData
from InfEngine.resources import engine_font_path, icon_path
from .engine import Engine, LogLevel
from .play_mode import PlayModeManager, PlayModeState
from .scene_manager import SceneFileManager

if not _PLAYER_MODE:
    from .resources_manager import ResourcesManager

# ── Editor-only imports ─────────────────────────────────────────────
# Skipped in standalone player builds (env _INFENGINE_PLAYER_MODE=1)
# to avoid pulling in the entire editor UI and keep Nuitka compilation
# fast and focused on player-relevant code only.

if not _PLAYER_MODE:
    from .ui import (
        MenuBarPanel,
        FrameSchedulerPanel,
        ToolbarPanel,
        HierarchyPanel,
        InspectorPanel,
        ConsolePanel,
        SceneViewPanel,
        GameViewPanel,
        ProjectPanel,
        WindowManager,
        TagLayerSettingsPanel,
        StatusBarPanel,
        BuildSettingsPanel,
        UIEditorPanel,
        EditorPanel,
        EditorServices,
        EditorEventBus,
        EditorEvent,
        PanelRegistry,
        editor_panel,
    )
    from .ui import panel_state as _panel_state


def _signal_engine_loaded() -> None:
    ready_file = os.environ.get("_INFENGINE_READY_FILE", "").strip()
    if ready_file:
        try:
            with open(ready_file, "w", encoding="utf-8") as f:
                f.write("ENGINE_LOADED\n")
                f.flush()
                os.fsync(f.fileno())
        except OSError:
            pass
    print("ENGINE_LOADED", flush=True)


def release_engine(project_path: str, engine_log_level=LogLevel.Info):
    """Launch InfEngine with Unity-style editor layout.

    Delegates to :class:`EditorBootstrap` for structured initialization.
    """
    import time
    from .bootstrap import EditorBootstrap
    bootstrap = EditorBootstrap(project_path, engine_log_level)
    bootstrap.run()

    bootstrap.engine.set_window_icon(icon_path)

    # Signal the launcher splash to begin its fade-out, then wait for it
    # to finish before revealing the engine window.
    _signal_engine_loaded()
    time.sleep(0.6)

    bootstrap.engine.show()
    bootstrap.engine.run()

    # ── Save panel states on exit ──
    _panel_state.put("console", bootstrap.console.save_state())
    _panel_state.put("project", bootstrap.project_panel.save_state())
    _panel_state.save()


def run_player(project_path: str, engine_log_level=LogLevel.Info):
    """Launch InfEngine in standalone player mode (no editor chrome).

    Opens the project's first scene from BuildSettings.json, applies the
    display mode from BuildManifest.json (fullscreen borderless or windowed
    with a custom resolution), plays the splash sequence if configured, then
    enters play mode and runs until the window is closed.
    """
    import json
    import time
    from .player_bootstrap import PlayerBootstrap

    # Read optional BuildManifest for display & splash settings
    manifest_path = os.path.join(project_path, "BuildManifest.json")
    manifest = {}
    if os.path.isfile(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8", errors="replace") as _f:
                manifest = json.load(_f)
        except Exception:
            pass

    display_mode = manifest.get("display_mode", "fullscreen_borderless")
    window_width = manifest.get("window_width", 1920)
    window_height = manifest.get("window_height", 1080)
    splash_items = manifest.get("splash_items", [])

    bootstrap = PlayerBootstrap(
        project_path, engine_log_level,
        display_mode=display_mode,
        window_width=window_width,
        window_height=window_height,
        splash_items=splash_items,
    )
    bootstrap.run()

    # Set window title to project name
    project_name = os.path.basename(os.path.normpath(project_path))
    bootstrap.engine.set_window_title(project_name)

    if display_mode == "fullscreen_borderless":
        bootstrap.engine.set_fullscreen(True)

    bootstrap.engine.set_window_icon(icon_path)

    _signal_engine_loaded()
    time.sleep(0.3)

    bootstrap.engine.show()
    bootstrap.engine.run()

__all__ = [
    "Engine",
    "LogLevel",
    "InfGUIRenderable",
    "InfGUIContext",
    "PlayModeManager",
    "PlayModeState",
    "SceneFileManager",
    "TextureLoader",
    "TextureData",
    "release_engine",
    "run_player",
]

if not _PLAYER_MODE:
    __all__ += [
        "ResourcesManager",
        "MenuBarPanel",
        "ToolbarPanel",
        "HierarchyPanel",
        "InspectorPanel",
        "ConsolePanel",
        "SceneViewPanel",
        "GameViewPanel",
        "UIEditorPanel",
        "ProjectPanel",
        "WindowManager",
        "TagLayerSettingsPanel",
        "StatusBarPanel",
        "BuildSettingsPanel",
        # Panel framework
        "EditorPanel",
        "EditorServices",
        "EditorEventBus",
        "EditorEvent",
        "PanelRegistry",
        "editor_panel",
    ]
