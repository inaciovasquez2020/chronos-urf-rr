#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

ART = Path("artifacts/chronos/reproducible_comparison_run_output_2026_06_01.json")
DOC = Path("docs/status/REPRODUCIBLE_COMPARISON_RUN_OUTPUT_2026_06_01.md")
RUNNER = Path("tools/run_gravity_baseline_model_comparison.py")
BASELINE = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")
MODEL = Path("artifacts/chronos/model_or_deficit_mass_vector_2026_06_01.json")
UNIT = Path("artifacts/chronos/unit_conversion_certificate_2026_06_01.json")
METRIC = Path("artifacts/chronos/predeclared_comparison_metric_2026_06_01.json")

REQUIRED_NON_CLAIMS = {
    "reproducible comparison run output only",
    "no empirical gravity result interpretation supplied",
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
    "CLAY_CLOSED_TRUE"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert RUNNER.exists(), f"missing runner: {RUNNER}"
    assert BASELINE.exists(), f"missing baseline: {BASELINE}"
    assert MODEL.exists(), f"missing model: {MODEL}"
    assert UNIT.exists(), f"missing unit: {UNIT}"
    assert METRIC.exists(), f"missing metric: {METRIC}"

    data = json.loads(ART.read_text())
    baseline = json.loads(BASELINE.read_text())
    model = json.loads(MODEL.read_text())
    unit = json.loads(UNIT.read_text())
    metric = json.loads(METRIC.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "REPRODUCIBLE_COMPARISON_RUN_OUTPUT_2026_06_01"
    assert data["object"] == "REPRODUCIBLE_COMPARISON_RUN_OUTPUT"
    assert data["status"] == "REPRODUCIBLE_COMPARISON_RUN_OUTPUT_SUPPLIED_NO_EMPIRICAL_INTERPRETATION"
    assert data["decision"] == "PASS"

    assert data["metric_id"] == metric["predeclared_metric"]["metric_id"]
    assert data["primary_metric"] == "canonical_rmse"
    assert data["vector_length"] == baseline["baseline_vector"]["length"]
    assert data["vector_length"] == model["model_or_deficit_mass_vector"]["length"]
    assert data["baseline_vector_sha256"] == baseline["baseline_vector"]["sha256"]
    assert data["model_or_deficit_mass_vector_sha256"] == model["model_or_deficit_mass_vector"]["sha256"]
    assert data["unit_conversion_artifact"] == unit["artifact"]

    assert data["reproducible_run_script_sha256"] == hashlib.sha256(RUNNER.read_bytes()).hexdigest()

    for key in [
        "canonical_rmse",
        "canonical_mae",
        "canonical_mean_signed_error",
        "canonical_max_abs_error",
    ]:
        assert isinstance(data[key], (int, float))
        assert math.isfinite(float(data[key]))

    assert data["run_output_supplied"] is True
    assert data["resolved_missing_input"] == "reproducible_comparison_run_output"
    assert data["remaining_missing_inputs"] == []
    assert data["remaining_missing_input_count"] == 0
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION"
    assert data["weakest_sufficient_next_input"] == "GravityBaselineVsModelComparisonResultInterpretation"

    print("REPRODUCIBLE_COMPARISON_RUN_OUTPUT_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "metric_id": data["metric_id"],
        "canonical_rmse": data["canonical_rmse"],
        "canonical_mae": data["canonical_mae"],
        "remaining_missing_input_count": data["remaining_missing_input_count"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
