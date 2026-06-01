#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/gravity_result_boundary_certificate_2026_06_01.json")
DOC = Path("docs/status/GRAVITY_RESULT_BOUNDARY_CERTIFICATE_2026_06_01.md")
PRIOR = Path("artifacts/chronos/gravity_baseline_vs_model_comparison_result_2026_06_01.json")

REQUIRED_MISSING = {
    "authenticated_gravity_payload",
    "coordinate_or_row_binding_certificate",
    "baseline_gravity_vector",
    "model_or_deficit_mass_vector",
    "unit_conversion_certificate",
    "predeclared_comparison_metric",
    "reproducible_comparison_run_output",
}

REQUIRED_NON_CLAIMS = {
    "no empirical comparison result",
    "no model-favored result",
    "no baseline-favored result",
    "no anomaly detection result",
    "no DFM-MKC validation",
    "no Lambda-CDM failure",
    "no dark matter resolution",
    "no dark energy resolution",
    "no physical discovery claim",
    "no unrestricted gravity theorem",
    "no Chronos-RR closure",
    "no H4.1/FGL closure",
    "no P vs NP claim",
    "no Clay-problem claim",
}

FORBIDDEN_CLAIMS = [
    "EMPIRICAL_GRAVITY_RESULT_CLOSED",
    "MODEL_FAVORED_RESULT_CLAIMED",
    "BASELINE_REFUTED",
    "ANOMALY_DETECTED",
    "DFM_MKC_VALIDATED",
    "LAMBDA_CDM_FAILED",
    "DARK_MATTER_RESOLVED",
    "DARK_ENERGY_RESOLVED",
    "CHRONOS_RR_CLOSED",
    "H4FGL_CLOSED",
    "P_VS_NP_CLOSED",
    "CLAY_CLOSED"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert PRIOR.exists(), f"missing prior artifact: {PRIOR}"

    data = json.loads(ART.read_text())
    prior = json.loads(PRIOR.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "GRAVITY_RESULT_BOUNDARY_CERTIFICATE_2026_06_01"
    assert data["object"] == "GRAVITY_RESULT_BOUNDARY_CERTIFICATE"
    assert data["status"] == "BOUNDARY_CERTIFICATE_FOR_TARGET_OPEN_COMPARISON"
    assert data["decision"] == "PASS"

    assert prior["object"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT"
    assert prior["status"] == "TARGET_OPEN_COMPARISON_INPUTS_NOT_SUPPLIED"
    assert prior["comparison_result_supplied"] is False

    assert data["certified_prior_status"] == prior["status"]
    assert data["empirical_result_supplied"] is False
    assert data["comparison_inputs_complete"] is False
    assert data["boundary_certificate_supplied"] is True

    assert REQUIRED_MISSING.issubset(set(data["certified_missing_inputs"]))
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for item in REQUIRED_MISSING:
        assert item in doc

    for item in REQUIRED_NON_CLAIMS:
        assert item in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "GLOBAL_URF_LAW3_RESTRICTED_VALID_KERNEL_INSTANCE"
    assert data["weakest_sufficient_next_input"] == "RestrictedValidKernelLaw3InstanceOrExplicitMissingLemma"

    print("GRAVITY_RESULT_BOUNDARY_CERTIFICATE_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "certified_prior_status": data["certified_prior_status"],
        "missing_input_count": len(data["certified_missing_inputs"]),
        "non_claim_count": len(data["certified_non_claims"]),
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
