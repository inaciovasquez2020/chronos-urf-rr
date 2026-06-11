from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_h41_certified_family_frontier_closed_lock() -> None:
    subprocess.run(
        ["python3", "tools/verify_h41_certified_family_frontier_closed_lock.py"],
        cwd=ROOT,
        check=True,
    )
