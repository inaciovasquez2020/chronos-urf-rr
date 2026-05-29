import subprocess
from pathlib import Path

def test_sparc_rotation_curve_step3_5_accounting_run_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_sparc_rotation_curve_step3_5_accounting_run.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "SPARC_STEP3_5_ACCOUNTING_RUN_AND_PREDICTIVE_TARGET_OK" in result.stdout
