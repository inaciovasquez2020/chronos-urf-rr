import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_gravity_active_carrier_binding_theorem_target_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_gravity_active_carrier_binding_theorem_target.py"],
        cwd=ROOT,
        check=True,
    )
