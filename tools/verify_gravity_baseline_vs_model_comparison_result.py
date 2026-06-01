#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/gravity_baseline_vs_model_comparison_result_2026_06_01.json")
DOC = Path("docs/status/GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_2026_06_01.md")

REQUIRED_FALSE_FIELDS = [
    "comparison_result_supplied",
    "authenticated_gravity_payload_supplied",
    "coordinate_or_row_binding_certificate_supplied",
    "baseline_gravity_vector_supplied",
    "model_or_deficit_mass_vector_supplied",
    "unit_conversion_certificate_supplied",
    "predeclared_comparison_metric_supplied",
    "reproducible_comparison_run_output_supplied",
]

REQUIRED_MISSING_INPUTS = [
    "authenticated_gravity_payload",
    "coordinate_or_row_binding_certificate",
    "baseline_gravity_vector",
    "model_or_deficit_mass_vector",
    "unit_conversion_certificate",
    "predeclared_comparison_metric",
    "reproducible_comparison_run_output",
]

REQUIRED_BOUNDARY_TOKENS = [
    "target artifact only",
    "no empirical comparison result supplied",
    "no model-favored result claimed",
    "no baseline-favored result claimed",
    "no gravity anomaly claim",
    "no dark matter claim",
    "no dark energy claim",
    "no DFM-MKC validation",
    "no Lambda-CDM failure",
    "no physical discovery claim",
    "no Chronos-RR theorem closure",
    "no H4.1/FGL closure",
    "no P vs NP claim",
    "no Clay-problem claim",
]

REQUIRED_OUTCOMES = [
    "MODEL_FAVORED_UNDER_PREDECLARED_METRIC",
    "NULL_OR_BASELINE_FAVORED",
    "INCONCLUSIVE_DUE_TO_BINDING_FAILURE",
    "INCONCLUSIVE_DUE_TO_ROW_MAPPING_FAILURE",
    "INCONCLUSIVE_DUE_TO_DATA_PROVENANCE_FAILURE",
    "INCONCLUSIVE_DUE_TO_UNIT_CONVERSION_FAILURE",
    "INCONCLUSIVE_DUE_TO_MISSING_MODEL_VECTOR",
    "INCONCLUSIVE_DUE_TO_MISSING_BASELINE_VECTOR",
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing status doc: {DOC}"

    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["artifact"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_2026_06_01"
    assert data["object"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT"
    assert data["status"] == "TARGET_OPEN_COMPARISON_INPUTS_NOT_SUPPLIED"
    assert data["decision"] == "PASS"

    for field in REQUIRED_FALSE_FIELDS:
        assert data[field] is False, f"{field} must remain false"

    for item in REQUIRED_MISSING_INPUTS:
        assert item in data["missing_inputs"], f"missing input not recorded: {item}"
        assert item in doc, f"missing input absent from doc: {item}"

    for token in REQUIRED_BOUNDARY_TOKENS:
        assert token in data["boundary"], f"missing boundary token: {token}"

    for outcome in REQUIRED_OUTCOMES:
        assert outcome in data["acceptable_outcomes"], f"missing acceptable outcome: {outcome}"
        assert outcome in doc, f"acceptable outcome absent from doc: {outcome}"

    assert data["next_admissible_object"] == "GRAVITY_RESULT_BOUNDARY_CERTIFICATE"
    assert data["weakest_sufficient_next_input"] == "CompleteGravityBaselineVsModelComparisonRunOutput"

    forbidden_positive_claims = [
        "GRAVITY_COMPARISON_RESULT_CLOSED",
        "MODEL_FAVORED_RESULT_CLAIMED",
        "BASELINE_REFUTED",
        "DARK_MATTER_RESOLVED",
        "DARK_ENERGY_RESOLVED",
        "DFM_MKC_VALIDATED",
        "LAMBDA_CDM_FAILED",
        "CLAY_CLOSED",
        "P_VS_NP_CLOSED",
    ]

    joined = json.dumps(data, sort_keys=True) + "\n" + doc
    for claim in forbidden_positive_claims:
        assert claim not in joined, f"forbidden positive claim present: {claim}"

    print("GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "missing_input_count": len(data["missing_inputs"]),
        "acceptable_outcome_count": len(data["acceptable_outcomes"]),
        "next_admissible_object": data["next_admissible_object"],
        "weakest_sufficient_next_input": data["weakest_sufficient_next_input"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
