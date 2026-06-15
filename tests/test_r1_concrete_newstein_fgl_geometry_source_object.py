from __future__ import annotations

import subprocess


def test_r1_concrete_newstein_fgl_geometry_source_object_verifier() -> None:
    result = subprocess.run(
        ["python3", "tools/verify_r1_concrete_newstein_fgl_geometry_source_object.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "R1_CONCRETE_NEWSTEIN_FGL_GEOMETRY_SOURCE_OBJECT_OK" in result.stdout
