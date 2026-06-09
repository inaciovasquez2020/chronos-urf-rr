from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_analytic_dini_estimate_binding_lemma_repository_local_envelope_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_analytic_dini_estimate_binding_lemma_repository_local_envelope.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ANALYTIC_DINI_ESTIMATE_BINDING_LEMMA_REPOSITORY_LOCAL_ENVELOPE_OK" in result.stdout
