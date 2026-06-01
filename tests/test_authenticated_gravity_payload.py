import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/authenticated_gravity_payload_2026_06_01.json")
DOC = Path("docs/status/AUTHENTICATED_GRAVITY_PAYLOAD_2026_06_01.md")
VERIFY = Path("tools/verify_authenticated_gravity_payload.py")

def test_artifact_records_authenticated_payload():
    data = json.loads(ART.read_text())
    assert data["object"] == "AUTHENTICATED_GRAVITY_PAYLOAD"
    assert data["decision"] == "PASS"
    assert data["resolved_missing_input"] == "authenticated_gravity_payload"

def test_digest_and_bytes_are_bound():
    data = json.loads(ART.read_text())
    assert data["sha256"] == "6554527f30e77923eae9f9793bcb315577551ad86ed763aa8a86110df463fd29"
    assert data["byte_count"] == 45289360
    assert data["payload_bytes_committed_to_git"] is False

def test_remaining_missing_inputs_are_six():
    data = json.loads(ART.read_text())
    assert data["remaining_missing_input_count"] == 6
    assert "coordinate_or_row_binding_certificate" in data["remaining_missing_inputs"]
    assert "reproducible_comparison_run_output" in data["remaining_missing_inputs"]

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "payload bytes are local external data and are not committed to git" in doc
    assert "no empirical gravity result supplied" in doc
    assert "no Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "AUTHENTICATED_GRAVITY_PAYLOAD_OK" in result.stdout
