"""Packaging tests for the installable ``scm-sim`` command (issue #30, SCM-F-043, SCM-NF-005)."""
import importlib
import shutil
import subprocess
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_pyproject() -> dict:
    with open(ROOT / "pyproject.toml", "rb") as f:
        return tomllib.load(f)


def test_pyproject_declares_scm_sim_console_script():
    scripts = load_pyproject()["project"]["scripts"]
    assert scripts["scm-sim"] == "scm_sim.__main__:main"
    module_name, func_name = scripts["scm-sim"].split(":")
    assert callable(getattr(importlib.import_module(module_name), func_name))


def test_package_has_no_runtime_dependencies():
    project = load_pyproject()["project"]
    assert project["dependencies"] == []
    assert project["requires-python"] == ">=3.11"


@pytest.mark.skipif(shutil.which("scm-sim") is None, reason="package not installed (pip install -e .)")
def test_installed_scm_sim_command_runs():
    result = subprocess.run(
        ["scm-sim", "--days", "10", "--seed", "42"], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr
    assert "=== Supply Chain Report: Day 10 ===" in result.stdout
