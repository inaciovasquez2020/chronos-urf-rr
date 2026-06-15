from __future__ import annotations

import subprocess


def test_r1_concrete_newstein_fgl_to_native_geometry_input_object_map_target_verifier() -> None:
    result = subprocess.run(
        ["python3", "tools/verify_r1_concrete_newstein_fgl_to_native_geometry_input_object_map_target.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "R1_CONCRETE_NEWSTEIN_FGL_TO_NATIVE_GEOMETRY_INPUT_OBJECT_MAP_TARGET_OK" in result.stdout
