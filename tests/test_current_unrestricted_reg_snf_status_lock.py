from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_current_unrestricted_reg_snf_status_lock_verifier_passes() -> None:
    subprocess.run(
        [sys.executable, "tools/verify_current_unrestricted_reg_snf_status_lock.py"],
        cwd=ROOT,
        check=True,
    )
