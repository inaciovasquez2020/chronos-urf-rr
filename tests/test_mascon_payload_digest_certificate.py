import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_payload_digest_certificate_2026_05_29.json")
DOC = Path("docs/status/MASCON_PAYLOAD_DIGEST_CERTIFICATE_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONPayloadDigestCertificate.lean")

def test_mascon_payload_digest_certificate_artifact_boundary():
    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "MASCON_PAYLOAD_DIGEST_CERTIFICATE_TARGET_ONLY_PAYLOAD_NOT_BOUND"
    assert artifact["payload_bytes_bound"] is False
    assert artifact["digest_bound"] is False
    assert artifact["collection_sha256"] is None
    assert artifact["file_count"] == 0
    assert artifact["total_bytes"] == 0
    assert artifact["weakest_missing_object"] == "AUTHENTICATED_MASCON_PAYLOAD_BYTES_AND_SHA256_DIGEST"

def test_mascon_payload_digest_certificate_doc_boundary():
    text = DOC.read_text()
    assert "Status: `MASCON_PAYLOAD_DIGEST_CERTIFICATE_TARGET_ONLY_PAYLOAD_NOT_BOUND`" in text
    assert "This is a target object only." in text
    assert "does not commit MASCON payload bytes" in text

def test_mascon_payload_digest_certificate_lean_boundary():
    text = LEAN.read_text()
    assert "deriving Repr, Inhabited" in text
    assert "mascon_payload_digest_certificate_payload_not_bound" in text
    assert "mascon_payload_digest_certificate_digest_not_bound" in text
    assert "mascon_payload_digest_certificate_status_lock" in text

def test_mascon_payload_digest_certificate_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_payload_digest_certificate.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_PAYLOAD_DIGEST_CERTIFICATE_OK" in result.stdout
