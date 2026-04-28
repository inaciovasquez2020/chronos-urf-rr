import subprocess
import sys
from pathlib import Path


def test_verify_urf_status_language_guard_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_urf_status_language_guard.py"],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "URF status language guard PASS" in result.stdout


def test_language_guard_has_boundary_and_forbidden_phrases():
    text = Path("tools/verify_urf_status_language_guard.py").read_text(
        encoding="utf-8"
    )

    assert "does not imply theorem-level closure" in text
    assert "Millennium solved" in text
    assert "unconditional closure" in text
    assert "Solved theorem surface" in text
