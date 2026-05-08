import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_fiber_mass_balance_frontier_verifier():
    subprocess.run(
        ["python3", "tools/verify_fiber_mass_balance_frontier.py"],
        cwd=ROOT,
        check=True,
    )
