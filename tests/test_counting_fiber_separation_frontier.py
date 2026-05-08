import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_counting_fiber_separation_frontier_verifier():
    subprocess.run(
        ["python3", "tools/verify_counting_fiber_separation_frontier.py"],
        cwd=ROOT,
        check=True,
    )
