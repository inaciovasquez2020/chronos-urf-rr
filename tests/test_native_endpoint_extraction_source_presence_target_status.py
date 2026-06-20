import subprocess
import sys

def test_native_endpoint_extraction_source_presence_target_status_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_native_endpoint_extraction_source_presence_target_status.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "NATIVE_ENDPOINT_EXTRACTION_SOURCE_PRESENCE_TARGET_STATUS_OK" in result.stdout
