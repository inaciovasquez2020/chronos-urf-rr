#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/non_null_physical_model_vector_or_deficit_mass_derivation_target_2026_06_01.json")
DOC = Path("docs/status/NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_TARGET_2026_06_01.md")
INTERP = Path("artifacts/chronos/gravity_baseline_vs_model_comparison_result_interpretation_2026_06_01.json")

REQUIRED_NON_CLAIMS = {
    "target only",
    "non-null physical model vector not supplied",
    "deficit-mass derivation not supplied",
    "current comparison remains null comparator only",
    "no empirical gravity result claim",
    "no anomaly detection claim",
    "no model-favored result claim",
    "no baseline-favored result claim",
    "no DFM-MKC validation",
    "no Lambda-CDM failure",
    "no dark matter resolution",
    "no dark energy resolution",
    "no physical discovery claim",
    "no Chronos-RR closure",
    "no H4.1/FGL closure",
    "no P vs NP claim",
    "no Clay-problem claim",
}

FORBIDDEN_CLAIMS = [
    "NON_NULL_PHYSICAL_MODEL_VECTOR_SUPPLIED_TRUE",
    "DEFICIT_MASS_DERIVATION_SUPPLIED_TRUE",
    "EMPIRICAL_GRAVITY_RESULT_SUPPLIED_TRUE",
    "ANOMALY_DETECTED_TRUE",
    "MODEL_FAVORED_RESULT_CLAIMED_TRUE",
    "DFM_MKC_VALIDATED_TRUE",
    "LAMBDA_CDM_FAILED_TRUE",
    "CLAY_CLOSED_TRUE"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert INTERP.exists(), f"missing interpretation artifact: {INTERP}"

    data = json.loads(ART.read_text())
    interp = json.loads(INTERP.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_TARGET_2026_06_01"
    assert data["object"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_TARGET"
    assert data["status"] == "TARGET_OPEN_NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_NOT_SUPPLIED"
    assert data["decision"] == "PASS"

    assert interp["object"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION"
    assert data["previous_result_class"] == "null_comparator_residual_recorded"
    assert data["previous_favored_result"] == "none"
    assert data["current_model_kind"] == "aligned_zero_null_vector"

    assert data["required_new_input"] == "NonNullPhysicalModelVectorOrDeficitMassDerivation"
    assert data["required_input_supplied"] is False
    assert data["current_model_is_physical"] is False
    assert data["current_model_is_deficit_mass_derivation"] is False

    assert len(data["required_input_schema"]["required_fields"]) >= 8
    assert len(data["required_input_schema"]["acceptance_predicates"]) >= 6
    assert len(data["blocked_downstream_without_required_input"]) >= 4

    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION"
    assert data["weakest_sufficient_next_input"] == "NonNullPhysicalModelVectorOrDeficitMassDerivation"

    print("NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_TARGET_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "required_input_supplied": data["required_input_supplied"],
        "current_model_kind": data["current_model_kind"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
