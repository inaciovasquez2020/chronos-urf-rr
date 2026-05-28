import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_extract_physical_detector_witness_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_extract_physical_detector_witness.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "EXTRACT_PHYSICAL_DETECTOR_WITNESS_OK" in result.stdout
