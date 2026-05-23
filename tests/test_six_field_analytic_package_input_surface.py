import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_six_field_analytic_package_input_surface_verifier():
    subprocess.run(
        ["python3", "tools/verify_six_field_analytic_package_input_surface.py"],
        cwd=ROOT,
        check=True,
    )
