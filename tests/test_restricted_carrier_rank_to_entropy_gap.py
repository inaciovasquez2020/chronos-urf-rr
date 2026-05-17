import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_carrier_rank_to_entropy_gap_verifier():
    subprocess.run(
        ["python3", "tools/verify_restricted_carrier_rank_to_entropy_gap.py"],
        cwd=ROOT,
        check=True,
    )
