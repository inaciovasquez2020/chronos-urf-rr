import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_selected_carrier_entropy_functional_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_selected_carrier_entropy_functional.py"],
        cwd=ROOT,
        check=True,
    )
