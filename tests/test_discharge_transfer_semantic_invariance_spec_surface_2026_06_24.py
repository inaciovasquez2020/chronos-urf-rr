import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_discharge_transfer_semantic_invariance_spec_surface_2026_06_24.py"

def test_discharge_transfer_semantic_invariance_spec_surface_verifier():
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_SPEC_SURFACE_2026_06_24_OK" in result.stdout
