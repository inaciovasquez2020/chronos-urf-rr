from __future__ import annotations

import subprocess


def test_r1_native_geometry_input_object_verifier() -> None:
    result = subprocess.run(
        ["python3", "tools/verify_r1_native_geometry_input_object.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "R1_NATIVE_GEOMETRY_INPUT_OBJECT_OK" in result.stdout
