from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_corrected_external_qk_dini_theorem1_payload_request_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_corrected_external_qk_dini_theorem1_payload_request.py"],
        cwd=ROOT,
        text=True,
        check=True,
        capture_output=True,
    )
    assert "CORRECTED_EXTERNAL_QK_DINI_THEOREM1_PAYLOAD_REQUEST_OK" in result.stdout
