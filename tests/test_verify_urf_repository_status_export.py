import subprocess
import sys
from pathlib import Path


def test_verify_urf_repository_status_export_script_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_urf_repository_status_export.py"],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "URF status export verification PASS" in result.stdout


def test_verify_urf_repository_status_export_script_is_committed_surface():
    p = Path("tools/verify_urf_repository_status_export.py")
    text = p.read_text(encoding="utf-8")

    assert "status-only seed registry" in text
    assert "does not imply theorem-level closure" in text
    assert "Solved theorem surface" in text
