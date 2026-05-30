import json
import subprocess
from pathlib import Path

def test_gracefo_schema_validation_execution_result_ci_portable():
    result = subprocess.run(
        ["python3", "tools/verify_gracefo_schema_validation_execution_result.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "GRACEFO_SCHEMA_VALIDATION_EXECUTION_RESULT_CI_PORTABLE_OK" in result.stdout

    digest = json.loads(Path(
        "artifacts/gracefo/authenticated_gracefo_payload_digest_certificate_2026_05_29.json"
    ).read_text())
    schema = json.loads(Path(
        "artifacts/gracefo/gracefo_schema_validation_execution_result_2026_05_29.json"
    ).read_text())

    assert digest["status"] == "AUTHENTICATED_GRACEFO_PAYLOAD_DIGEST_CERTIFICATE_CREATED"
    assert schema["status"] == "GRACEFO_SCHEMA_VALIDATION_EXECUTION_RESULT_CREATED"
    assert digest["collection_sha256"] == schema["collection_sha256"]
    assert schema["schema_checks"]["period_count"] == 2
    assert schema["schema_checks"]["data_file_count"] == 12
