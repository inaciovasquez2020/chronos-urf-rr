import subprocess
import sys

def test_physical_detector_field_extraction_map():
    subprocess.run([sys.executable, "tools/verify_physical_detector_field_extraction_map.py"], check=True)
