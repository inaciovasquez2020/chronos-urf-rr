from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_external_qk_dini_coefficient_extraction_rule_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_external_qk_dini_coefficient_extraction_rule.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "EXTERNAL_QK_DINI_COEFFICIENT_EXTRACTION_RULE_OK" in result.stdout
