import subprocess
import sys


def test_spherical_null_expansion_criterion_surface_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_spherical_null_expansion_criterion_surface.py"],
        check=True,
    )
