from pathlib import Path
import subprocess
import sys


def test_r1_native_map_remaining_evidence_obligation_rank():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_native_map_remaining_evidence_obligation_rank.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "R1_NATIVE_MAP_REMAINING_EVIDENCE_OBLIGATION_RANK_OK" in result.stdout
