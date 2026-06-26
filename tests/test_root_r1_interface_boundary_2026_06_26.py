import subprocess
from pathlib import Path

def test_root_r1_interface_boundary_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_root_r1_interface_boundary_2026_06_26.py"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "ROOT_R1_INTERFACE_BOUNDARY_2026_06_26_OK" in result.stdout
