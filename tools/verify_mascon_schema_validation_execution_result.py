#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ART = Path("artifacts/gravity/mascon_schema_validation_execution_result_2026_05_29.json")
DOC = Path("docs/status/MASCON_SCHEMA_VALIDATION_EXECUTION_RESULT_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONSchemaValidationExecutionResult.lean")
DIGEST = Path("artifacts/gravity/authenticated_mascon_payload_digest_2026_05_29.json")

EXPECTED_STATUS = "MASCON_SCHEMA_VALIDATION_EXECUTED"
EXPECTED_NEXT = "MASCON_MODEL_COMPARISON_EXECUTION_TARGET"

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing doc: {DOC}")
    require(LEAN.exists(), f"missing Lean module: {LEAN}")
    require(DIGEST.exists(), f"missing digest artifact: {DIGEST}")

    artifact = json.loads(ART.read_text())
    digest = json.loads(DIGEST.read_text())
    doc = DOC.read_text()
    lean = LEAN.read_text()

    require(artifact["status"] == EXPECTED_STATUS, "bad status")
    require(artifact["predecessor"] == "AUTHENTICATED_MASCON_PAYLOAD_DIGEST_2026_05_29", "bad predecessor")
    require(artifact["matches_authenticated_digest_manifest"] is True, "digest manifest mismatch flag")
    require(artifact["schema_validation_passed"] is True, "schema validation did not pass")
    require(artifact["required_dimensions_present"] is True, "required dimensions missing")
    require(artifact["required_coordinate_variables_present"] is True, "required coordinate variables missing")
    require(artifact["dimension_count"] >= 3, "dimension count too small")
    require(artifact["variable_count"] >= 4, "variable count too small")
    require(artifact["grid_variable_count"] > 0, "no grid variables")
    require(artifact["time_dependent_grid_variable_count"] > 0, "no time-dependent grid variables")
    require(artifact["next_admissible_object"] == EXPECTED_NEXT, "bad next object")

    for name in ["time", "lat", "lon"]:
        require(name in artifact["dimensions"], f"missing dimension: {name}")
        require(name in artifact["variables"], f"missing coordinate variable: {name}")

    require(len(artifact["payload_sha256"]) == 64, "payload SHA256 must be hex")
    require(any(entry["sha256"] == artifact["payload_sha256"] for entry in digest["manifest"]), "payload SHA256 absent from digest manifest")

    payload = Path(artifact["payload_path"])
    local_payload_files_present = payload.exists()
    if local_payload_files_present:
        data = payload.read_bytes()
        require(len(data) == artifact["payload_size_bytes"], "local payload size mismatch")
        require(hashlib.sha256(data).hexdigest() == artifact["payload_sha256"], "local payload SHA256 mismatch")

    for token in [
        EXPECTED_STATUS,
        EXPECTED_NEXT,
        "schema validation only",
        "payload bytes are local only and not committed to git",
        "no empirical gravity result is asserted",
        "no Clay problem claim is asserted",
    ]:
        require(token in json.dumps(artifact) or token in doc or token in lean, f"missing token: {token}")

    print("MASCON_SCHEMA_VALIDATION_EXECUTION_RESULT_OK")
    print(json.dumps({
        "status": artifact["status"],
        "schema_validation_passed": artifact["schema_validation_passed"],
        "dimension_count": artifact["dimension_count"],
        "variable_count": artifact["variable_count"],
        "payload_sha256": artifact["payload_sha256"],
        "local_payload_files_present": local_payload_files_present,
        "next_admissible_object": artifact["next_admissible_object"],
    }, indent=2))

if __name__ == "__main__":
    main()
