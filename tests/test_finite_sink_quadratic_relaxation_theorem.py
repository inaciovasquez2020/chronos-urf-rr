import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_finite_sink_quadratic_relaxation_theorem_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_finite_sink_quadratic_relaxation_theorem.py"],
        cwd=ROOT,
        check=True,
    )
