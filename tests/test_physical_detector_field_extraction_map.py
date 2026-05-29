import subprocess
from pathlib import Path


def test_physical_detector_field_extraction_map_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_physical_detector_field_extraction_map.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_OK" in result.stdout
