import subprocess
import sys

def test_native_endpoint_extraction_selected_semantic_source_target_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_native_endpoint_extraction_selected_semantic_source_target.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "NATIVE_ENDPOINT_EXTRACTION_SELECTED_SEMANTIC_SOURCE_TARGET_OK" in result.stdout
