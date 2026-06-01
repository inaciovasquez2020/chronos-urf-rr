#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/gravity_empirical_result_inputs_missing_certificate_2026_06_01.json")
DOC = Path("docs/status/GRAVITY_EMPIRICAL_RESULT_INPUTS_MISSING_CERTIFICATE_2026_06_01.md")
TARGET = Path("artifacts/chronos/gravity_baseline_vs_model_comparison_result_2026_06_01.json")
BOUNDARY = Path("artifacts/chronos/gravity_result_boundary_certificate_2026_06_01.json")

MISSING_INPUTS = {
    "authenticated_gravity_payload",
    "coordinate_or_row_binding_certificate",
    "baseline_gravity_vector",
    "model_or_deficit_mass_vector",
    "unit_conversion_certificate",
    "predeclared_comparison_metric",
    "reproducible_comparison_run_output",
}

FALSE_FIELDS = [
    "empirical_gravity_result_supplied",
    "authenticated_gravity_payload_supplied",
    "coordinate_or_row_binding_certificate_supplied",
    "baseline_gravity_vector_supplied",
    "model_or_deficit_mass_vector_supplied",
    "unit_conversion_certificate_supplied",
    "predeclared_comparison_metric_supplied",
    "reproducible_comparison_run_output_supplied",
]

REQUIRED_NON_CLAIMS = {
    "no empirical gravity result supplied",
    "no authenticated gravity payload supplied",
    "no coordinate or row binding certificate supplied",
    "no baseline gravity vector supplied",
    "no model or deficit-mass vector supplied",
    "no unit conversion certificate supplied",
    "no predeclared comparison metric supplied",
    "no reproducible comparison run output supplied",
    "no model-favored result",
    "no baseline-favored result",
    "no anomaly detection result",
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
    "EMPIRICAL_GRAVITY_RESULT_SUPPLIED_TRUE",
    "AUTHENTICATED_GRAVITY_PAYLOAD_SUPPLIED_TRUE",
    "GRAVITY_COMPARISON_CLOSED",
    "MODEL_FAVORED_RESULT_CLAIMED",
    "BASELINE_FAVORED_RESULT_CLAIMED",
    "ANOMALY_DETECTED",
    "DFM_MKC_VALIDATED",
    "LAMBDA_CDM_FAILED",
    "DARK_MATTER_RESOLVED",
    "DARK_ENERGY_RESOLVED",
    "CLAY_CLOSED"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert TARGET.exists(), f"missing prior target: {TARGET}"
    assert BOUNDARY.exists(), f"missing boundary certificate: {BOUNDARY}"

    data = json.loads(ART.read_text())
    target = json.loads(TARGET.read_text())
    boundary = json.loads(BOUNDARY.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "GRAVITY_EMPIRICAL_RESULT_INPUTS_MISSING_CERTIFICATE_2026_06_01"
    assert data["object"] == "GRAVITY_EMPIRICAL_RESULT_INPUTS_MISSING_CERTIFICATE"
    assert data["status"] == "EXPLICIT_EMPIRICAL_INPUTS_MISSING_NO_RESULT_SUPPLIED"
    assert data["decision"] == "PASS"

    assert target["object"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT"
    assert target["status"] == "TARGET_OPEN_COMPARISON_INPUTS_NOT_SUPPLIED"
    assert boundary["object"] == "GRAVITY_RESULT_BOUNDARY_CERTIFICATE"
    assert boundary["status"] == "BOUNDARY_CERTIFICATE_FOR_TARGET_OPEN_COMPARISON"

    for field in FALSE_FIELDS:
        assert data[field] is False, f"field should remain false: {field}"

    assert MISSING_INPUTS.issubset(set(data["missing_inputs"]))
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in MISSING_INPUTS:
        assert token in doc

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "AUTHENTICATED_GRAVITY_PAYLOAD_OR_COMPLETE_GRAVITY_BASELINE_VS_MODEL_COMPARISON_RUN_OUTPUT"
    assert data["weakest_sufficient_next_input"] == "AuthenticatedGravityPayload"

    print("GRAVITY_EMPIRICAL_RESULT_INPUTS_MISSING_CERTIFICATE_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "missing_input_count": len(data["missing_inputs"]),
        "non_claim_count": len(data["certified_non_claims"]),
        "next_admissible_object": data["next_admissible_object"],
        "weakest_sufficient_next_input": data["weakest_sufficient_next_input"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
