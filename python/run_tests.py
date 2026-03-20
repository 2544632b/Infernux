"""Run Python tests and point developers at manual physics regressions."""

import os
import sys
import subprocess


def _run_pytest(test_root: str) -> int:
    import pytest  # noqa: F401

    return subprocess.call([sys.executable, "-m", "pytest", test_root])


def _run_unittest(test_root: str) -> int:
    return subprocess.call([sys.executable, "-m", "unittest", "discover", "-s", test_root, "-p", "test_*.py"])


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_root = os.path.join(script_dir, "test")
    if not os.path.isdir(test_root):
        legacy_root = os.path.join(script_dir, "InfEngine", "test")
        if os.path.isdir(legacy_root):
            test_root = legacy_root

    code = _run_pytest(test_root)
    if code == -1:
        print("pytest not found, falling back to unittest discovery.")
        code = _run_unittest(test_root)

    manual_suite = os.path.join(script_dir, "InfEngine", "test", "physics_regression_suite.py")
    if os.path.isfile(manual_suite):
        print("Manual physics regression suite:", manual_suite)

    return code


if __name__ == "__main__":
    raise SystemExit(main())
