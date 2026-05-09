import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_selected_carrier_nontrivial_counting_frontier_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_selected_carrier_nontrivial_counting_frontier.py"],
        cwd=ROOT,
        check=True,
    )
