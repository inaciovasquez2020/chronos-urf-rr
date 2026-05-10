import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_final_carrier_observation_extraction_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_final_carrier_observation_extraction.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Final carrier observation extraction closure verified." in result.stdout
