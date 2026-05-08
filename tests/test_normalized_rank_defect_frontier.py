import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_normalized_rank_defect_frontier_verifier():
    subprocess.run(
        ["python3", "tools/verify_normalized_rank_defect_frontier.py"],
        cwd=ROOT,
        check=True,
    )
