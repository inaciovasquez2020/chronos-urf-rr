import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_rank_rate_gap_axiomatic_bridge_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_rank_rate_gap_axiomatic_bridge.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "RankRateGap axiomatic bridge verified." in result.stdout
