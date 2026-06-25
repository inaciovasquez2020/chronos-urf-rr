import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_defect_repair_normalization_target_2026_06_24.py"

def test_defect_repair_normalization_target_verifier():
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "DEFECT_REPAIR_NORMALIZATION_TARGET_2026_06_24_OK" in result.stdout
