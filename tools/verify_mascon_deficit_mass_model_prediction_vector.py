#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/mascon_deficit_mass_model_prediction_vector_2026_05_29.json")
DOC = Path("docs/status/MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONDeficitMassModelPredictionVector.lean")
BASELINE = Path("artifacts/gravity/mascon_baseline_gravity_model_prediction_vector_2026_05_29.json")

EXPECTED_STATUS = "MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR_TARGET_ONLY_NO_LAW"
EXPECTED_NEXT = "CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW"

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing doc: {DOC}")
    require(LEAN.exists(), f"missing Lean module: {LEAN}")
    require(BASELINE.exists(), f"missing baseline artifact: {BASELINE}")

    artifact = json.loads(ART.read_text())
    baseline = json.loads(BASELINE.read_text())
    doc = DOC.read_text()
    lean = LEAN.read_text()

    require(baseline["baseline_prediction_vector_bound"] is True, "baseline vector predecessor not bound")
    require(artifact["status"] == EXPECTED_STATUS, "bad status")
    require(artifact["predecessor"] == "MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR_2026_05_29", "bad predecessor")
    require(artifact["baseline_prediction_vector_bound"] is True, "baseline flag must be true")
    require(artifact["deficit_mass_prediction_vector_bound"] is False, "deficit vector must not be bound")
    require(artifact["concrete_deficit_mass_law_bound"] is False, "concrete law must not be bound")
    require(artifact["prediction_vector_materialized"] is False, "prediction vector must not be materialized")
    require(artifact["comparison_metric_bound"] is False, "comparison metric must not be bound")
    require(artifact["model_comparison_executed"] is False, "comparison must not be executed")
    require(artifact["weakest_missing_object"] == EXPECTED_NEXT, "bad weakest missing object")
    require(artifact["next_admissible_object"] == EXPECTED_NEXT, "bad next object")

    required = set(artifact["required_inputs"])
    for name in [
        "CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW",
        "MASCON_GRID_TO_DEFICIT_MASS_OPERATOR",
        "MASCON_DEFICIT_MASS_VECTOR_GENERATOR",
        "MASCON_DEFICIT_MASS_VECTOR_DIGEST",
    ]:
        require(name in required, f"missing required input: {name}")

    for token in [
        EXPECTED_STATUS,
        EXPECTED_NEXT,
        "target object only",
        "no deficit-mass prediction vector is bound",
        "no concrete deficit-mass prediction law is supplied",
        "no empirical gravity result is asserted",
        "no Clay problem claim is asserted",
    ]:
        require(token in json.dumps(artifact) or token in doc or token in lean, f"missing token: {token}")

    print("MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR_TARGET_OK")
    print(json.dumps({
        "status": artifact["status"],
        "baseline_prediction_vector_bound": artifact["baseline_prediction_vector_bound"],
        "deficit_mass_prediction_vector_bound": artifact["deficit_mass_prediction_vector_bound"],
        "weakest_missing_object": artifact["weakest_missing_object"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
