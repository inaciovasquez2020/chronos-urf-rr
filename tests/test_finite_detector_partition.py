import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_finite_detector_partition_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_finite_detector_partition.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "FINITE_DETECTOR_PARTITION_OK" in result.stdout
