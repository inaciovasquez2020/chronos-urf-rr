import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_unrestricted_witness_carrier_input_target_2026_06_24.py"

def test_unrestricted_witness_carrier_input_target_verifier():
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "UNRESTRICTED_WITNESS_CARRIER_INPUT_TARGET_2026_06_24_OK" in result.stdout
