from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_terminal_admissible_boundary_chain_certificate_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_terminal_admissible_boundary_chain_certificate.py"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "TERMINAL_ADMISSIBLE_BOUNDARY_CHAIN_CERTIFICATE_OK" in result.stdout
    assert "BOUNDARY=CLOSED_NO_THEOREM_PROMOTION_VERIFIER_ONLY" in result.stdout
