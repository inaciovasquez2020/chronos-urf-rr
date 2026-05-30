import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/authenticated_mascon_payload_digest_2026_05_29.json")
DOC = Path("docs/status/AUTHENTICATED_MASCON_PAYLOAD_DIGEST_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/AuthenticatedMASCONPayloadDigest.lean")

def test_authenticated_mascon_payload_digest_artifact():
    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "AUTHENTICATED_MASCON_PAYLOAD_DIGEST_BOUND_BYTES_NOT_COMMITTED"
    assert artifact["target_id"] == "AUTHENTICATED_MASCON_PAYLOAD_BYTES_AND_SHA256_DIGEST"
    assert artifact["payload_bytes_bound"] is True
    assert artifact["digest_bound"] is True
    assert artifact["payload_bytes_committed_to_git"] is False
    assert artifact["file_count"] > 0
    assert artifact["total_bytes"] > 0
    assert len(artifact["collection_sha256"]) == 64
    assert artifact["next_admissible_object"] == "MASCON_SCHEMA_VALIDATION_EXECUTION_RESULT"

def test_authenticated_mascon_payload_digest_doc_boundary():
    text = DOC.read_text()
    assert "Status: `AUTHENTICATED_MASCON_PAYLOAD_DIGEST_BOUND_BYTES_NOT_COMMITTED`" in text
    assert "Payload bytes are locally hashed but not committed to git." in text
    assert "MASCON_SCHEMA_VALIDATION_EXECUTION_RESULT" in text

def test_authenticated_mascon_payload_digest_lean_boundary():
    text = LEAN.read_text()
    assert "AuthenticatedMASCONPayloadDigestCertificate" in text
    assert "authenticated_mascon_payload_digest_payload_bound" in text
    assert "authenticated_mascon_payload_digest_digest_bound" in text
    assert "authenticated_mascon_payload_digest_bytes_not_committed" in text
    assert "authenticated_mascon_payload_digest_status_lock" in text

def test_authenticated_mascon_payload_digest_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_authenticated_mascon_payload_digest.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "AUTHENTICATED_MASCON_PAYLOAD_DIGEST_OK" in result.stdout
