from __future__ import annotations

import subprocess


def test_r1_uniform_local_type_capacity_discharge_target_verifier() -> None:
    result = subprocess.run(
        ["python3", "tools/verify_r1_uniform_local_type_capacity_discharge_target.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "R1_UNIFORM_LOCAL_TYPE_CAPACITY_DISCHARGE_TARGET_OK" in result.stdout
