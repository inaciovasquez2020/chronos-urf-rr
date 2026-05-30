#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/mascon_payload_digest_certificate_2026_05_29.json")
DOC = Path("docs/status/MASCON_PAYLOAD_DIGEST_CERTIFICATE_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONPayloadDigestCertificate.lean")

EXPECTED_STATUS = "MASCON_PAYLOAD_DIGEST_CERTIFICATE_TARGET_ONLY_PAYLOAD_NOT_BOUND"
EXPECTED_MISSING = "AUTHENTICATED_MASCON_PAYLOAD_BYTES_AND_SHA256_DIGEST"

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing doc: {DOC}")
    require(LEAN.exists(), f"missing Lean module: {LEAN}")

    artifact = json.loads(ART.read_text())
    doc = DOC.read_text()
    lean = LEAN.read_text()

    require(artifact["status"] == EXPECTED_STATUS, "bad artifact status")
    require(artifact["registry_id"] == "NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_2026_05_29", "bad registry id")
    require(artifact["target_id"] == "MASCON_PAYLOAD_DIGEST_CERTIFICATE", "bad target id")
    require(artifact["payload_bytes_bound"] is False, "payload bytes must remain unbound")
    require(artifact["digest_bound"] is False, "digest must remain unbound")
    require(artifact["collection_sha256"] is None, "collection sha256 must be null")
    require(artifact["file_count"] == 0, "file count must be zero")
    require(artifact["total_bytes"] == 0, "total bytes must be zero")
    require(artifact["weakest_missing_object"] == EXPECTED_MISSING, "bad weakest missing object")

    for token in [
        EXPECTED_STATUS,
        EXPECTED_MISSING,
        "no MASCON payload bytes are committed",
        "no MASCON SHA256 digest is supplied",
        "no empirical gravity result is asserted",
        "no Clay problem claim is asserted",
    ]:
        require(token in json.dumps(artifact) or token in doc or token in lean, f"missing token: {token}")

    print("MASCON_PAYLOAD_DIGEST_CERTIFICATE_OK")
    print(json.dumps({
        "status": artifact["status"],
        "payload_bytes_bound": artifact["payload_bytes_bound"],
        "digest_bound": artifact["digest_bound"],
        "weakest_missing_object": artifact["weakest_missing_object"],
        "artifact": str(ART)
    }, indent=2))

if __name__ == "__main__":
    main()
