import subprocess
import sys
from pathlib import Path


def test_nonsymmetric_collapse_censorship_hoop_frontiers_verifier():
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, "tools/verify_nonsymmetric_collapse_censorship_hoop_frontiers.py"],
        cwd=root,
        check=True,
    )
