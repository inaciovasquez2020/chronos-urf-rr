from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_repository_local_qk_dini_source_object_payload_value_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_repository_local_qk_dini_source_object_payload_value.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "REPOSITORY_LOCAL_QK_DINI_SOURCE_OBJECT_PAYLOAD_VALUE_OK" in result.stdout
