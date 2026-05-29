from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_theta_residual_predictive_holdout_execution_run.py"

def test_theta_residual_predictive_holdout_execution_run_verifier() -> None:
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "THETA_RESIDUAL_PREDICTIVE_HOLDOUT_EXECUTION_RUN_OK" in result.stdout
