#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ART = Path("artifacts/gravity/authenticated_mascon_payload_digest_2026_05_29.json")
DOC = Path("docs/status/AUTHENTICATED_MASCON_PAYLOAD_DIGEST_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/AuthenticatedMASCONPayloadDigest.lean")

EXPECTED_STATUS = "AUTHENTICATED_MASCON_PAYLOAD_DIGEST_BOUND_BYTES_NOT_COMMITTED"
EXPECTED_TARGET = "AUTHENTICATED_MASCON_PAYLOAD_BYTES_AND_SHA256_DIGEST"
EXPECTED_NEXT = "MASCON_SCHEMA_VALIDATION_EXECUTION_RESULT"

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def recompute_collection(manifest):
    canonical = "\n".join(
        f"{e['path']}\0{e['size_bytes']}\0{e['sha256']}"
        for e in manifest
    ).encode()
    return hashlib.sha256(canonical).hexdigest()

def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing doc: {DOC}")
    require(LEAN.exists(), f"missing Lean module: {LEAN}")

    artifact = json.loads(ART.read_text())
    doc = DOC.read_text()
    lean = LEAN.read_text()

    require(artifact["status"] == EXPECTED_STATUS, "bad status")
    require(artifact["target_id"] == EXPECTED_TARGET, "bad target")
    require(artifact["payload_bytes_bound"] is True, "payload bytes must be bound")
    require(artifact["digest_bound"] is True, "digest must be bound")
    require(artifact["payload_bytes_committed_to_git"] is False, "payload bytes must not be committed")
    require(artifact["file_count"] > 0, "file_count must be positive")
    require(artifact["total_bytes"] > 0, "total_bytes must be positive")
    require(isinstance(artifact["collection_sha256"], str), "collection_sha256 must be string")
    require(len(artifact["collection_sha256"]) == 64, "collection_sha256 must be SHA256 hex")
    require(artifact["next_admissible_object"] == EXPECTED_NEXT, "bad next object")
    require(len(artifact["manifest"]) == artifact["file_count"], "manifest length mismatch")
    require(recompute_collection(artifact["manifest"]) == artifact["collection_sha256"], "collection digest mismatch")

    local_payload_files_present = True
    for entry in artifact["manifest"]:
        require(len(entry["sha256"]) == 64, f"bad sha256 for {entry['path']}")
        local = Path(entry["path"])
        if local.exists():
            data = local.read_bytes()
            require(len(data) == entry["size_bytes"], f"local size mismatch: {local}")
            require(hashlib.sha256(data).hexdigest() == entry["sha256"], f"local sha256 mismatch: {local}")
        else:
            local_payload_files_present = False

    for token in [
        EXPECTED_STATUS,
        EXPECTED_TARGET,
        EXPECTED_NEXT,
        "payload bytes are locally hashed but not committed to git",
        "no empirical gravity result is asserted",
        "no Clay problem claim is asserted",
    ]:
        require(token in json.dumps(artifact) or token in doc or token in lean, f"missing token: {token}")

    print("AUTHENTICATED_MASCON_PAYLOAD_DIGEST_OK")
    print(json.dumps({
        "status": artifact["status"],
        "file_count": artifact["file_count"],
        "total_bytes": artifact["total_bytes"],
        "collection_sha256": artifact["collection_sha256"],
        "next_admissible_object": artifact["next_admissible_object"],
        "local_payload_files_present": local_payload_files_present
    }, indent=2))

if __name__ == "__main__":
    main()
