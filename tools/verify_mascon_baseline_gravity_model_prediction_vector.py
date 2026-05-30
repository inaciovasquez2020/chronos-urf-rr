#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ART = Path("artifacts/gravity/mascon_baseline_gravity_model_prediction_vector_2026_05_29.json")
DOC = Path("docs/status/MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONBaselineGravityModelPredictionVector.lean")
SCHEMA = Path("artifacts/gravity/mascon_schema_validation_execution_result_2026_05_29.json")
TARGET = Path("artifacts/gravity/mascon_model_comparison_execution_target_2026_05_29.json")

EXPECTED_STATUS = "MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR_BOUND_CONTROL_ONLY"
EXPECTED_NEXT = "MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR"

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def expected_digest(schema, time_count, lat_count, lon_count, vector_length):
    canonical = (
        "MASCON_BASELINE_ZERO_ANOMALY_VECTOR\n"
        f"predecessor={schema['id']}\n"
        f"payload_sha256={schema['payload_sha256']}\n"
        f"shape={time_count},{lat_count},{lon_count}\n"
        f"length={vector_length}\n"
        "value=0.0\n"
    ).encode()
    return hashlib.sha256(canonical).hexdigest()

def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing doc: {DOC}")
    require(LEAN.exists(), f"missing Lean module: {LEAN}")
    require(SCHEMA.exists(), f"missing schema artifact: {SCHEMA}")
    require(TARGET.exists(), f"missing target artifact: {TARGET}")

    artifact = json.loads(ART.read_text())
    schema = json.loads(SCHEMA.read_text())
    target = json.loads(TARGET.read_text())
    doc = DOC.read_text()
    lean = LEAN.read_text()

    require(schema["schema_validation_passed"] is True, "schema predecessor not passed")
    require(target["status"] == "MASCON_MODEL_COMPARISON_EXECUTION_TARGET_ONLY_NO_MODEL_RUN", "bad target predecessor")
    require(artifact["status"] == EXPECTED_STATUS, "bad status")
    require(artifact["baseline_prediction_vector_bound"] is True, "baseline vector must be bound")
    require(artifact["prediction_vector_materialized"] is False, "vector must not be materialized")
    require(artifact["prediction_vector_generator"] == "constant_zero", "bad generator")
    require(artifact["prediction_value"] == 0.0, "bad prediction value")
    require(artifact["deficit_mass_prediction_vector_bound"] is False, "deficit vector must not be bound")
    require(artifact["comparison_metric_bound"] is False, "comparison metric must not be bound")
    require(artifact["model_comparison_executed"] is False, "comparison must not be executed")
    require(artifact["weakest_missing_object"] == EXPECTED_NEXT, "bad weakest missing object")
    require(artifact["next_admissible_object"] == EXPECTED_NEXT, "bad next object")

    time_count = artifact["shape"]["time"]
    lat_count = artifact["shape"]["lat"]
    lon_count = artifact["shape"]["lon"]
    require(time_count == schema["dimensions"]["time"]["size"], "time shape mismatch")
    require(lat_count == schema["dimensions"]["lat"]["size"], "lat shape mismatch")
    require(lon_count == schema["dimensions"]["lon"]["size"], "lon shape mismatch")

    vector_length = time_count * lat_count * lon_count
    require(artifact["vector_length"] == vector_length, "vector length mismatch")
    require(
        artifact["vector_generator_sha256"] == expected_digest(schema, time_count, lat_count, lon_count, vector_length),
        "vector generator digest mismatch"
    )

    for token in [
        EXPECTED_STATUS,
        EXPECTED_NEXT,
        "ZERO_ANOMALY_CONTROL_BASELINE_ON_AUTHENTICATED_MASCON_GRID",
        "baseline control vector only",
        "no MASCON model comparison is executed",
        "no empirical gravity result is asserted",
        "no Clay problem claim is asserted",
    ]:
        require(token in json.dumps(artifact) or token in doc or token in lean, f"missing token: {token}")

    print("MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR_OK")
    print(json.dumps({
        "status": artifact["status"],
        "baseline_model_id": artifact["baseline_model_id"],
        "shape": artifact["shape"],
        "vector_length": artifact["vector_length"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
