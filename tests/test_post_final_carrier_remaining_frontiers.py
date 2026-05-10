import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_post_final_carrier_remaining_frontiers_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_post_final_carrier_remaining_frontiers.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Post-final-carrier remaining frontiers verified." in result.stdout
