from __future__ import annotations

import subprocess


def test_hep_t_external_notation_classification_verifier() -> None:
    result = subprocess.run(
        ["python3", "tools/verify_hep_t_external_notation_classification.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "HEP_T_EXTERNAL_NOTATION_CLASSIFICATION_OK" in result.stdout
