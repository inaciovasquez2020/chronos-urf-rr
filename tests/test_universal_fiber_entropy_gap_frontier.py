import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_universal_fiber_entropy_gap_frontier_verifier():
    subprocess.run(
        ["python3", "tools/verify_universal_fiber_entropy_gap_frontier.py"],
        cwd=ROOT,
        check=True,
    )
