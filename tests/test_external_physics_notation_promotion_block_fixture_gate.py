from __future__ import annotations

import subprocess


def test_external_physics_notation_promotion_block_fixture_gate_verifier() -> None:
    result = subprocess.run(
        [
            "python3",
            "tools/verify_external_physics_notation_promotion_block_fixture_gate.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "EXTERNAL_PHYSICS_NOTATION_PROMOTION_BLOCK_FIXTURE_GATE_OK" in result.stdout
