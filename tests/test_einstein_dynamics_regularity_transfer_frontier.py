import subprocess
import sys
from pathlib import Path


def test_einstein_dynamics_regularity_transfer_frontier_verifier():
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, "tools/verify_einstein_dynamics_regularity_transfer_frontier.py"],
        cwd=root,
        check=True,
    )
