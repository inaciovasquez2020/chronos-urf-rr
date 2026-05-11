from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_zero_arity_conditional_verifier_passes() -> None:
    subprocess.run(
        [sys.executable, "tools/verify_zero_arity_carrier_exhaustiveness_conditional.py"],
        cwd=ROOT,
        check=True,
    )


def test_zero_arity_numerical_sanity_passes() -> None:
    completed = subprocess.run(
        [sys.executable, "tools/numerical_zero_arity_carrier_exhaustiveness.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["status"] == "NUMERICAL_SANITY_ONLY"
    assert payload["theorem_level_closure"] is False
    assert payload["zero_arity_count"] == 2
    assert payload["failures"] == []
