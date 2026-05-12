from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_repository_native_finite_registry_exhaustiveness_from_fintype_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_repository_native_finite_registry_exhaustiveness_from_fintype.py"],
        cwd=ROOT,
        check=True,
    )
