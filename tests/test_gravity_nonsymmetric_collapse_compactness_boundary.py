import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_gravity_nonsymmetric_collapse_compactness_boundary_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_gravity_nonsymmetric_collapse_compactness_boundary.py"],
        cwd=ROOT,
        check=True,
    )
