from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_concrete_scientific_qk_dini_source_object_payload_gate_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_concrete_scientific_qk_dini_source_object_payload_gate.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "CONCRETE_SCIENTIFIC_QK_DINI_SOURCE_OBJECT_PAYLOAD_GATE_OK" in result.stdout
