import subprocess
from pathlib import Path

ROOT = Path.cwd()


def test_final_carrier_generated_projection_verifier():
    subprocess.run(
        ["python3", "tools/verify_final_carrier_generated_projection.py"],
        cwd=ROOT,
        check=True,
    )
