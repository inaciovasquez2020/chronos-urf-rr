from pathlib import Path
import subprocess
import sys


def test_r1_concrete_newstein_fgl_to_native_map_long_chord_input_field():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_concrete_newstein_fgl_to_native_map_long_chord_input_field.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "R1_CONCRETE_NEWSTEIN_FGL_TO_NATIVE_MAP_LONG_CHORD_INPUT_FIELD_OK" in result.stdout
