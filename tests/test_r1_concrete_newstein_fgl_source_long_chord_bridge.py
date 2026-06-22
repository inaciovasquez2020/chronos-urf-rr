from pathlib import Path
import subprocess
import sys


def test_r1_concrete_newstein_fgl_source_long_chord_bridge():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_concrete_newstein_fgl_source_long_chord_bridge.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "R1_CONCRETE_NEWSTEIN_FGL_SOURCE_LONG_CHORD_BRIDGE_OK" in result.stdout
