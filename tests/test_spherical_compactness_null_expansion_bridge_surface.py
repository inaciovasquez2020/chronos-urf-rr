import subprocess
import sys


def test_spherical_compactness_null_expansion_bridge_surface_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_spherical_compactness_null_expansion_bridge_surface.py"],
        check=True,
    )
