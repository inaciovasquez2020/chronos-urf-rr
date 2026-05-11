from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_repository_native_zero_arity_migration_target_verifier_passes() -> None:
    subprocess.run(
        [sys.executable, "tools/verify_repository_native_zero_arity_migration_target.py"],
        cwd=ROOT,
        check=True,
    )


def test_repository_native_zero_arity_migration_artifact_boundary() -> None:
    payload = json.loads(
        (ROOT / "artifacts/chronos/repository_native_zero_arity_carrier_migration_target_2026_05_11.json").read_text()
    )

    assert payload["status"] == "FRONTIER_OPEN / REPOSITORY_NATIVE_INTERFACE_REDUCTION_ONLY"
    assert payload["theorem_level_closure"] is False
    assert payload["unrestricted_chronos_rr_closure"] is False
    assert payload["h4_1_fgl_closure"] is False
    assert payload["universal_fiber_entropy_gap_closure"] is False
    assert payload["p_vs_np_closure"] is False
    assert payload["clay_problem_closure"] is False
    assert "repository-native Carrier satisfies the interface" in payload["not_proved_in_this_artifact"]
