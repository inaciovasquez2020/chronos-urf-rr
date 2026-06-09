from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_external_qk_dini_name_resolution_certificate_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_external_qk_dini_name_resolution_certificate.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "EXTERNAL_QK_DINI_NAME_RESOLUTION_CERTIFICATE_OK" in result.stdout
