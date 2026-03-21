from __future__ import annotations

import argparse
import ctypes
import os
import platform
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile


def _is_python312(python_exe: str) -> bool:
    if not os.path.isfile(python_exe):
        return False

    kwargs = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
    }
    if sys.platform == "win32":
        kwargs["creationflags"] = 0x08000000

    try:
        completed = subprocess.run(
            [python_exe, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            timeout=20,
            **kwargs,
        )
    except (OSError, subprocess.SubprocessError):
        return False

    return completed.returncode == 0 and (completed.stdout or "").strip() == "3.12"


def _find_installed_python(python_root: str) -> str | None:
    direct_candidates = [
        os.path.join(python_root, "python.exe"),
        os.path.join(python_root, "Python.exe"),
        os.path.join(python_root, "Python312", "python.exe"),
        os.path.join(python_root, "bin", "python"),
    ]
    for candidate in direct_candidates:
        if _is_python312(candidate):
            return candidate

    for root, _dirs, files in os.walk(python_root):
        for filename in files:
            if filename.lower() != "python.exe":
                continue
            candidate = os.path.join(root, filename)
            if _is_python312(candidate):
                return candidate

    return None


_GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"


def _runtime_zip_info_for_machine() -> tuple[str, str]:
    """Return (filename, url) for the Python 3.12 embeddable zip package."""
    machine = (platform.machine() or "").lower()
    if machine in {"amd64", "x86_64"}:
        return (
            "python-3.12.8-embed-amd64.zip",
            "https://www.python.org/ftp/python/3.12.8/python-3.12.8-embed-amd64.zip",
        )
    if machine in {"arm64", "aarch64"}:
        return (
            "python-3.12.8-embed-arm64.zip",
            "https://www.python.org/ftp/python/3.12.8/python-3.12.8-embed-arm64.zip",
        )
    if machine in {"x86", "i386", "i686"}:
        return (
            "python-3.12.8-embed-win32.zip",
            "https://www.python.org/ftp/python/3.12.8/python-3.12.8-embed-win32.zip",
        )
    raise RuntimeError(f"Unsupported Windows architecture: {machine}")


def _download_file(url: str, dest: str) -> None:
    """Download a file from *url* to *dest*."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "InfEngine-Hub-Installer/1.0")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as f:
            shutil.copyfileobj(resp, f)
    except urllib.error.URLError as exc:
        if "unknown url type: https" in str(exc).lower():
            raise RuntimeError(
                "HTTPS download support is unavailable. "
                "The SSL runtime was not initialized correctly."
            ) from exc
        raise


def _enable_site_packages(python_root: str) -> None:
    """Uncomment 'import site' in the ._pth file to enable site-packages."""
    for name in os.listdir(python_root):
        if name.endswith("._pth"):
            pth_path = os.path.join(python_root, name)
            with open(pth_path, "r", encoding="utf-8") as f:
                content = f.read()
            content = content.replace("#import site", "import site")
            with open(pth_path, "w", encoding="utf-8") as f:
                f.write(content)
            break


def _run_hidden(args: list[str], *, timeout: int) -> None:
    kwargs = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
    }
    if sys.platform == "win32":
        kwargs["creationflags"] = 0x08000000

    completed = subprocess.run(args, timeout=timeout, **kwargs)
    if completed.returncode != 0:
        details = (completed.stderr or completed.stdout or "").strip()
        raise RuntimeError(
            f"Command failed with exit code {completed.returncode}: {' '.join(args)}\n{details}"
        )


def _show_message_box(title: str, message: str, icon: int = 0x40) -> None:
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.user32.MessageBoxW(None, message, title, icon)
    except Exception:
        pass


def _emit(progress_callback, message: str) -> None:
    if progress_callback is not None:
        progress_callback(message)


def install_runtime_for_app(app_dir: str, progress_callback=None) -> None:
    zip_name, zip_url = _runtime_zip_info_for_machine()
    hub_data_dir = os.path.join(app_dir, "InfEngineHubData")
    runtime_dir = os.path.join(hub_data_dir, "runtime")
    python_root = os.path.join(hub_data_dir, "python312")
    template_dir = os.path.join(runtime_dir, "venv_template")
    zip_path = os.path.join(runtime_dir, zip_name)
    python_exe = os.path.join(python_root, "python.exe")
    get_pip_path = os.path.join(runtime_dir, "get-pip.py")

    os.makedirs(runtime_dir, exist_ok=True)

    # 1. Download the embeddable zip (skipped if already cached).
    if not os.path.isfile(zip_path):
        _emit(progress_callback, f"Downloading Python 3.12 for {platform.machine()}...")
        _download_file(zip_url, zip_path)

    # 2. Extract into python312/.
    if not os.path.isfile(python_exe):
        _emit(progress_callback, "Extracting Python 3.12...")
        shutil.rmtree(python_root, ignore_errors=True)
        os.makedirs(python_root, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(python_root)

    if not os.path.isfile(python_exe):
        raise RuntimeError(
            "Python 3.12 executable was not found after extraction:\n"
            f"{python_exe}"
        )

    # 3. Enable site-packages in the ._pth file.
    _emit(progress_callback, "Configuring Python runtime...")
    _enable_site_packages(python_root)

    # 4. Bootstrap pip via get-pip.py.
    pip_exe = os.path.join(python_root, "Scripts", "pip.exe")
    if not os.path.isfile(pip_exe):
        if not os.path.isfile(get_pip_path):
            _emit(progress_callback, "Downloading pip bootstrap...")
            _download_file(_GET_PIP_URL, get_pip_path)
        _emit(progress_callback, "Installing pip...")
        _run_hidden([python_exe, get_pip_path, "--no-warn-script-location"], timeout=600)

    # 5. Install virtualenv (used in place of stdlib venv which the embeddable
    #    distribution does not include).
    _emit(progress_callback, "Installing virtualenv...")
    _run_hidden(
        [python_exe, "-m", "pip", "install", "virtualenv", "-q", "--no-warn-script-location"],
        timeout=600,
    )

    # 6. Create the reusable venv template.
    _emit(progress_callback, "Preparing reusable venv template...")
    shutil.rmtree(template_dir, ignore_errors=True)
    _run_hidden([python_exe, "-m", "virtualenv", "--copies", template_dir], timeout=600)
    _emit(progress_callback, "Private runtime is ready.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-dir")
    args = parser.parse_args()

    if not args.app_dir:
        _show_message_box(
            "InfEngine Runtime Installer",
            "This program is an internal installer helper for InfEngine Hub.\n\n"
            "Please run InfEngineHubInstaller.exe instead of launching this file directly.",
            0x30,
        )
        return 1

    install_runtime_for_app(args.app_dir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        _show_message_box(
            "InfEngine Runtime Installer Error",
            str(exc),
            0x10,
        )
        try:
            sys.stderr.write(str(exc) + "\n")
        except Exception:
            pass
        raise SystemExit(1)