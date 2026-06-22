from pathlib import Path
import subprocess
import sys


def test_r1_uniform_local_type_capacity_discharge_target_missing_evidence_boundary():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_uniform_local_type_capacity_discharge_target_missing_evidence_boundary.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "R1_UNIFORM_LOCAL_TYPE_CAPACITY_DISCHARGE_TARGET_MISSING_EVIDENCE_BOUNDARY_OK" in result.stdout
