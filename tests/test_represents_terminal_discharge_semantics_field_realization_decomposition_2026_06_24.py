import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_represents_terminal_discharge_semantics_field_realization_decomposition_2026_06_24.py"

def test_represents_terminal_discharge_semantics_field_realization_decomposition_verifier():
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_DECOMPOSITION_2026_06_24_OK" in result.stdout
