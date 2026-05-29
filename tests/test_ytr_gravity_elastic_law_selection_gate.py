import subprocess
import sys


def test_ytr_gravity_elastic_law_selection_gate_verifier():
    result = subprocess.run(
        [sys.executable, "tools/verify_ytr_gravity_elastic_law_selection_gate.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "YTR_GRAVITY_ELASTIC_LAW_SELECTION_GATE_OK" in result.stdout
