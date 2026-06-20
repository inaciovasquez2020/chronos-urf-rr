import subprocess
import sys


def test_r1_width_threshold_alias_surface_verifier():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_width_threshold_alias_surface.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "R1_WIDTH_THRESHOLD_ALIAS_SURFACE_OK" in result.stdout
