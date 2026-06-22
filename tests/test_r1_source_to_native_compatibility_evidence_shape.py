from pathlib import Path
import subprocess
import sys


def test_r1_source_to_native_compatibility_evidence_shape():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_source_to_native_compatibility_evidence_shape.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "R1_SOURCE_TO_NATIVE_COMPATIBILITY_EVIDENCE_SHAPE_OK" in result.stdout
