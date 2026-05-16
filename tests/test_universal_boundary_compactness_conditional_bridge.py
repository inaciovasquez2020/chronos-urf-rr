import subprocess
import sys
from pathlib import Path


def test_universal_boundary_compactness_conditional_bridge_verifier():
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, "tools/verify_universal_boundary_compactness_conditional_bridge.py"],
        cwd=root,
        check=True,
    )
