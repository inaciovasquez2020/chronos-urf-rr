#!/usr/bin/env python3
import json
import math
from pathlib import Path

ART = Path("artifacts/chronos/gravity_baseline_vs_model_comparison_result_interpretation_2026_06_01.json")
DOC = Path("docs/status/GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION_2026_06_01.md")
RUNOUT = Path("artifacts/chronos/reproducible_comparison_run_output_2026_06_01.json")
MODEL = Path("artifacts/chronos/model_or_deficit_mass_vector_2026_06_01.json")

REQUIRED_NON_CLAIMS = {
    "comparison result interpretation only",
    "null comparator residual recorded only",
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
    "EMPIRICAL_GRAVITY_RESULT_SUPPLIED_TRUE",
    "ANOMALY_DETECTED_TRUE",
    "MODEL_FAVORED_RESULT_CLAIMED_TRUE",
    "BASELINE_FAVORED_RESULT_CLAIMED_TRUE",
    "DFM_MKC_VALIDATED_TRUE",
    "LAMBDA_CDM_FAILED_TRUE",
    "DARK_MATTER_RESOLVED_TRUE",
    "DARK_ENERGY_RESOLVED_TRUE",
    "PHYSICAL_DISCOVERY_CLAIMED_TRUE",
    "CLAY_CLOSED_TRUE"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert RUNOUT.exists(), f"missing run output: {RUNOUT}"
    assert MODEL.exists(), f"missing model vector: {MODEL}"

    data = json.loads(ART.read_text())
    runout = json.loads(RUNOUT.read_text())
    model = json.loads(MODEL.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION_2026_06_01"
    assert data["object"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION"
    assert data["status"] == "NULL_COMPARATOR_RESULT_INTERPRETED_NO_EMPIRICAL_OR_PHYSICAL_CLAIM"
    assert data["decision"] == "PASS"

    assert runout["object"] == "REPRODUCIBLE_COMPARISON_RUN_OUTPUT"
    assert model["object"] == "MODEL_OR_DEFICIT_MASS_VECTOR"

    assert data["source_run_output"]["run_output_sha256"] == runout["run_output_sha256"]
    assert data["source_run_output"]["metric_id"] == runout["metric_id"]
    assert data["source_run_output"]["canonical_rmse"] == runout["canonical_rmse"]

    assert data["model_classification"]["model_kind"] == "aligned_zero_null_vector"
    assert data["model_classification"]["not_physical_model"] is True
    assert data["model_classification"]["not_deficit_mass_derivation"] is True

    interp = data["interpretation"]
    assert interp["kind"] == "null-comparator metric interpretation"
    assert interp["result_class"] == "null_comparator_residual_recorded"
    assert interp["favored_result"] == "none"
    assert interp["empirical_claim"] == "none"
    assert isinstance(interp["primary_metric_value"], (int, float))
    assert math.isfinite(float(interp["primary_metric_value"]))

    assert data["remaining_missing_inputs"] == []
    assert data["remaining_missing_input_count"] == 0
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in [
        "comparison result interpretation only",
        "null comparator residual",
        "empirical gravity result",
        "model-favored result",
        "DFM-MKC validation",
        "Clay-problem result",
    ]:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION"
    assert data["weakest_sufficient_next_input"] == "NonNullPhysicalModelVectorOrDeficitMassDerivation"

    print("GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "primary_metric_value": interp["primary_metric_value"],
        "result_class": interp["result_class"],
        "favored_result": interp["favored_result"],
        "remaining_missing_input_count": data["remaining_missing_input_count"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
