from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_external_source_theorem_certificate_one_axiom_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_external_source_theorem_certificate_one_axiom.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "EXTERNAL_SOURCE_THEOREM_CERTIFICATE_PAYLOAD_REQUIRED_OK" in result.stdout
