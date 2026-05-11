from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_exhaustive_zero_arity_finite_model_check_passes() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "tools/exhaustive_zero_arity_carrier_finite_model_check.py",
            "--max-arity",
            "12",
            "--tag-count",
            "64",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["status"] == "FINITE_MODEL_EXHAUSTIVE_PROOF_ONLY"
    assert payload["finite_universe"]["carrier_count"] == 64 * 13
    assert payload["zero_arity_count"] == 64
    assert payload["failures"] == []
    assert payload["theorem_level_closure"] is False
    assert "no unrestricted Chronos-RR closure" in payload["boundary"]
