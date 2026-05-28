import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_physical_field_data_finite_samples_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_physical_field_data_finite_samples.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "PHYSICAL_FIELD_DATA_FINITE_SAMPLES_OK" in result.stdout
