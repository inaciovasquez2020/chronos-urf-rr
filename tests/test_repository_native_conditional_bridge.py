from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_repository_native_conditional_bridge_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_repository_native_conditional_bridge.py"],
        cwd=ROOT,
        check=True,
    )


def test_repository_native_conditional_bridge_tracks_lowercase_lean_path() -> None:
    tracked = subprocess.check_output(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
    ).splitlines()

    assert "chronos/Frontier/RepositoryNativeConditionalBridge.lean" in tracked
    assert "Chronos/Frontier/RepositoryNativeConditionalBridge.lean" not in tracked
