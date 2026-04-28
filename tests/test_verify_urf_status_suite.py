import subprocess
import sys
from pathlib import Path


def test_verify_urf_status_suite_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_urf_status_suite.py"],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "URF status export verification PASS" in result.stdout
    assert "URF status language guard PASS" in result.stdout
    assert "URF status suite PASS" in result.stdout


def test_verify_urf_status_suite_tracks_required_checks():
    text = Path("tools/verify_urf_status_suite.py").read_text(encoding="utf-8")

    assert "tools/verify_urf_repository_status_export.py" in text
    assert "tools/verify_urf_status_language_guard.py" in text
