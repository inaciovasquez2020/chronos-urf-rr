import subprocess
import sys


def test_spherical_collapse_gate_threshold_surface_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_spherical_collapse_gate_threshold_surface.py"],
        check=True,
    )
