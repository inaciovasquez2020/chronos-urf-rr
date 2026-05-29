#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/concrete_mascon_deficit_mass_prediction_law_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/ConcreteMASCONDeficitMassPredictionLaw.lean")
DOC = Path("docs/status/CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW_2026_05_29.md")

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert DOC.exists(), f"missing status doc: {DOC}"

    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "CONCRETE_LAW_INTERFACE_ONLY_NO_EMPIRICAL_MODEL_RUN"
    assert artifact["prediction_vector_bound"] is False
    assert artifact["model_comparison_executed"] is False

    boundary = artifact["boundary"]
    required = [
        "no_empirical_gravity_result",
        "no_gr_failure_claim",
        "no_new_gravity_claim",
        "no_dark_matter_replacement",
        "no_lambda_cdm_failure",
        "no_quantum_gravity",
        "no_clay_problem",
    ]
    for key in required:
        assert boundary[key] is True, key

    print("CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW_OK")
    print(json.dumps({
        "status": artifact["status"],
        "prediction_vector_bound": artifact["prediction_vector_bound"],
        "model_comparison_executed": artifact["model_comparison_executed"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
