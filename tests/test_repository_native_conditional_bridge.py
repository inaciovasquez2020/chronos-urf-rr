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


def test_repository_native_conditional_bridge_lean_compiles() -> None:
    subprocess.run(
        ["lake", "env", "lean", "chronos/Frontier/RepositoryNativeConditionalBridge.lean"],
        cwd=ROOT,
        check=True,
    )
