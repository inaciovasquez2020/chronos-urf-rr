from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_zero_arity_exhaustiveness_to_reg_snf_bridge_verifier_passes() -> None:
    subprocess.run(
        [sys.executable, "tools/verify_zero_arity_exhaustiveness_to_reg_snf_bridge.py"],
        cwd=ROOT,
        check=True,
    )
