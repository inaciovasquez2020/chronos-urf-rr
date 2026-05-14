import subprocess
import sys

def test_fo4_radius_r_type_enumeration_surface_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fo4_radius_r_type_enumeration_surface.py"],
        check=True,
    )
