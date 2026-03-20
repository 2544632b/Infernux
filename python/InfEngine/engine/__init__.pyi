from __future__ import annotations

from typing import Any, Callable, Optional

from InfEngine.lib import InfGUIRenderable, InfGUIContext, TextureLoader, TextureData
from InfEngine.engine.engine import Engine, LogLevel
from InfEngine.engine.resources_manager import ResourcesManager
from InfEngine.engine.play_mode import PlayModeManager, PlayModeState
from InfEngine.engine.scene_manager import SceneFileManager
from InfEngine.engine.ui import (
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


def release_engine(project_path: str, engine_log_level: LogLevel = ...) -> None: ...


__all__ = [
    "Engine",
    "LogLevel",
    "InfGUIRenderable",
    "InfGUIContext",
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
    "PlayModeManager",
    "PlayModeState",
    "SceneFileManager",
    "TextureLoader",
    "TextureData",
    "release_engine",
    "ResourcesManager",
    "BuildSettingsPanel",
    "EditorPanel",
    "EditorServices",
    "EditorEventBus",
    "EditorEvent",
    "PanelRegistry",
    "editor_panel",
]
