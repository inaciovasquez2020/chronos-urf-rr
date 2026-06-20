import subprocess
import sys

def test_native_endpoint_extraction_source_presence_status_doc_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_native_endpoint_extraction_source_presence_status_doc.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "NATIVE_ENDPOINT_EXTRACTION_SOURCE_PRESENCE_STATUS_DOC_OK" in result.stdout
