#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/mascon_model_comparison_execution_target_2026_05_29.json")
DOC = Path("docs/status/MASCON_MODEL_COMPARISON_EXECUTION_TARGET_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONModelComparisonExecutionTarget.lean")
SCHEMA = Path("artifacts/gravity/mascon_schema_validation_execution_result_2026_05_29.json")

EXPECTED_STATUS = "MASCON_MODEL_COMPARISON_EXECUTION_TARGET_ONLY_NO_MODEL_RUN"
EXPECTED_NEXT = "MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR"

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing doc: {DOC}")
    require(LEAN.exists(), f"missing Lean module: {LEAN}")
    require(SCHEMA.exists(), f"missing schema artifact: {SCHEMA}")

    artifact = json.loads(ART.read_text())
    schema = json.loads(SCHEMA.read_text())
    doc = DOC.read_text()
    lean = LEAN.read_text()

    require(schema["schema_validation_passed"] is True, "predecessor schema validation not passed")
    require(artifact["status"] == EXPECTED_STATUS, "bad status")
    require(artifact["predecessor"] == "MASCON_SCHEMA_VALIDATION_EXECUTION_RESULT_2026_05_29", "bad predecessor")
    require(artifact["schema_validation_passed"] is True, "schema validation flag must be true")
    require(artifact["model_comparison_executed"] is False, "model comparison must not be executed")
    require(artifact["baseline_prediction_vector_bound"] is False, "baseline vector must not be bound")
    require(artifact["deficit_mass_prediction_vector_bound"] is False, "deficit-mass vector must not be bound")
    require(artifact["comparison_metric_bound"] is False, "comparison metric must not be bound")
    require(artifact["weakest_missing_object"] == EXPECTED_NEXT, "bad weakest missing object")
    require(artifact["next_admissible_object"] == EXPECTED_NEXT, "bad next object")

    for token in [
        EXPECTED_STATUS,
        EXPECTED_NEXT,
        "MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR",
        "MASCON_COMPARISON_METRIC_SPECIFICATION",
        "execution target only",
        "no MASCON model comparison is executed",
        "no empirical gravity result is asserted",
        "no Clay problem claim is asserted",
    ]:
        require(token in json.dumps(artifact) or token in doc or token in lean, f"missing token: {token}")

    print("MASCON_MODEL_COMPARISON_EXECUTION_TARGET_OK")
    print(json.dumps({
        "status": artifact["status"],
        "schema_validation_passed": artifact["schema_validation_passed"],
        "model_comparison_executed": artifact["model_comparison_executed"],
        "weakest_missing_object": artifact["weakest_missing_object"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
