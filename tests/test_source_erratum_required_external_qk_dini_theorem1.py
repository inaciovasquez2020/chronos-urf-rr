from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_source_erratum_required_external_qk_dini_theorem1_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_source_erratum_required_external_qk_dini_theorem1.py"],
        cwd=ROOT,
        text=True,
        check=True,
        capture_output=True,
    )
    assert "SOURCE_ERRATUM_REQUIRED_EXTERNAL_QK_DINI_THEOREM1_OK" in result.stdout
