import datetime
import os
import sys
import json
import venv
import subprocess
import shutil
import glob
from pathlib import Path

from hub_utils import is_frozen


def _find_dev_wheel() -> str:
    """Find the InfEngine wheel in the dist/ directory next to the engine source.

    Only used in dev mode (non-frozen).
    """
    engine_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dist_dir = os.path.join(engine_root, "dist")
    wheels = glob.glob(os.path.join(dist_dir, "infengine-*.whl"))
    if wheels:
        wheels.sort(key=os.path.getmtime, reverse=True)
        return wheels[0]
    return ""


class ProjectModel:
    def __init__(self, db, version_manager=None):
        self.db = db
        self.version_manager = version_manager

    def add_project(self, name, path):
        return self.db.add_project(name, path)

    def delete_project(self, name):
        self.db.delete_project(name)

    
    def init_project_folder(self, project_name: str, project_path: str,
                            engine_version: str = ""):
        project_dir = os.path.join(project_path, project_name)
        os.makedirs(project_dir, exist_ok=True)

        # Create subdirectories
        for subdir in ("ProjectSettings", "Logs", "Library", "Assets"):
            os.makedirs(os.path.join(project_dir, subdir), exist_ok=True)

        # Create a README file in assets
        readme_path = os.path.join(project_dir, "Assets", "README.md")
        with open(readme_path, "w") as f:
            f.write("# Project Assets\n\nThis folder contains all the assets for the project.\n")

        # Create .ini file in project path
        ini_path = os.path.join(project_dir, f"{project_name}.ini")
        now = datetime.datetime.now()
        with open(ini_path, "w", encoding="utf-8") as f:
            f.write("[Project]\n")
            f.write(f"name = {project_name}\n")
            f.write(f"path = {project_dir}\n")
            f.write(f"created_at = {now}\n")
            f.write(f"changed_at = {now}\n")

        # ── Pin engine version ──────────────────────────────────────────
        if engine_version:
            from version_manager import VersionManager
            VersionManager.write_project_version(project_dir, engine_version)

        # ── Create .venv and install InfEngine ──────────────────────────
        venv_path = os.path.join(project_dir, ".venv")
        venv.EnvBuilder(with_pip=True).create(venv_path)
        self._install_infengine_in_venv(project_dir, engine_version)

        # ── Create VS Code workspace configuration ─────────────────────
        self._create_vscode_workspace(project_dir)

    # -----------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------

    @staticmethod
    def _get_venv_python(project_dir: str) -> str:
        """Return the Python executable inside the project's .venv."""
        venv_dir = os.path.join(project_dir, ".venv")
        if sys.platform == "win32":
            return os.path.join(venv_dir, "Scripts", "python.exe")
        return os.path.join(venv_dir, "bin", "python")

    @staticmethod
    def _install_infengine_in_venv(project_dir: str, engine_version: str = ""):
        """Install the InfEngine wheel into the project's .venv.

        In frozen (packaged Hub) mode, the wheel comes from the version
        manager cache (~/.infengine/versions/<ver>/).
        In dev mode, we try the local dist/ wheel first, then fall back
        to an editable install from the source tree.
        """
        venv_python = ProjectModel._get_venv_python(project_dir)
        if not os.path.isfile(venv_python):
            print(f"[ProjectModel] venv python not found: {venv_python}")
            return

        wheel = ""

        if is_frozen() and engine_version:
            # Packaged Hub — use the version manager cache
            from version_manager import VersionManager
            vm = VersionManager()
            wheel = vm.get_wheel_path(engine_version) or ""

        if not wheel:
            wheel = _find_dev_wheel()

        if wheel:
            subprocess.run(
                [venv_python, "-m", "pip", "install", "--force-reinstall", wheel],
                capture_output=True,
            )
            print(f"[ProjectModel] Installed InfEngine from wheel: {wheel}")
        else:
            # Dev fallback: editable install from source tree
            engine_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            subprocess.run(
                [venv_python, "-m", "pip", "install", "-e", engine_root],
                capture_output=True,
            )
            print(f"[ProjectModel] Installed InfEngine (editable) from: {engine_root}")

    @staticmethod
    def _create_vscode_workspace(project_dir: str):
        """
        Create .vscode/ config so that opening any file inside the project
        uses the correct Python interpreter and gets full InfEngine autocompletion.
        """
        vscode_dir = os.path.join(project_dir, ".vscode")
        os.makedirs(vscode_dir, exist_ok=True)

        # ── settings.json ───────────────────────────────────────────────
        venv_python = ProjectModel._get_venv_python(project_dir)
        settings = {
            "python.defaultInterpreterPath": venv_python,
            "python.analysis.typeCheckingMode": "basic",
            "python.analysis.autoImportCompletions": True,
            "python.analysis.diagnosticSeverityOverrides": {
                "reportMissingModuleSource": "none",
            },
            "editor.formatOnSave": True,
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                "**/*.meta": True,
                ".venv": True,
                "Library": True,
                "Logs": True,
                "ProjectSettings": True,
            },
        }
        settings_path = os.path.join(vscode_dir, "settings.json")
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)

        # ── extensions.json ─────────────────────────────────────────────
        extensions = {
            "recommendations": [
                "ms-python.python",
                "ms-python.vscode-pylance",
            ]
        }
        extensions_path = os.path.join(vscode_dir, "extensions.json")
        with open(extensions_path, "w", encoding="utf-8") as f:
            json.dump(extensions, f, indent=4, ensure_ascii=False)

        # ── pyrightconfig.json (at project root) ────────────────────────
        pyright_config = {
            "venvPath": ".",
            "venv": ".venv",
            "pythonVersion": "3.12",
            "typeCheckingMode": "basic",
            "reportMissingModuleSource": False,
            "reportWildcardImportFromLibrary": False,
            "include": ["Assets"],
        }
        pyright_path = os.path.join(project_dir, "pyrightconfig.json")
        with open(pyright_path, "w", encoding="utf-8") as f:
            json.dump(pyright_config, f, indent=4, ensure_ascii=False)