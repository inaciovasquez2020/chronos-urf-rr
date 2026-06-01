#!/usr/bin/env python3
import json
import math
from pathlib import Path

ART = Path("artifacts/chronos/predeclared_comparison_metric_2026_06_01.json")
DOC = Path("docs/status/PREDECLARED_COMPARISON_METRIC_2026_06_01.md")
AUTH = Path("artifacts/chronos/authenticated_gravity_payload_2026_06_01.json")
COORD = Path("artifacts/chronos/coordinate_or_row_binding_certificate_2026_06_01.json")
BASELINE = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")
MODEL = Path("artifacts/chronos/model_or_deficit_mass_vector_2026_06_01.json")
UNIT = Path("artifacts/chronos/unit_conversion_certificate_2026_06_01.json")

EXPECTED_REMAINING = {
    "reproducible_comparison_run_output",
}

REQUIRED_NON_CLAIMS = {
    "predeclared comparison metric only",
    "no reproducible comparison run output supplied",
    "no empirical gravity result supplied",
    "no anomaly detection result",
    "no model-favored result",
    "no baseline-favored result",
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
    "REPRODUCIBLE_COMPARISON_RUN_OUTPUT_SUPPLIED_TRUE",
    "EMPIRICAL_GRAVITY_RESULT_SUPPLIED_TRUE",
    "ANOMALY_DETECTED",
    "MODEL_FAVORED_RESULT_CLAIMED",
    "BASELINE_FAVORED_RESULT_CLAIMED",
    "DFM_MKC_VALIDATED",
    "LAMBDA_CDM_FAILED",
    "CLAY_CLOSED"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert AUTH.exists(), f"missing authenticated payload artifact: {AUTH}"
    assert COORD.exists(), f"missing coordinate artifact: {COORD}"
    assert BASELINE.exists(), f"missing baseline artifact: {BASELINE}"
    assert MODEL.exists(), f"missing model artifact: {MODEL}"
    assert UNIT.exists(), f"missing unit artifact: {UNIT}"

    data = json.loads(ART.read_text())
    auth = json.loads(AUTH.read_text())
    coord = json.loads(COORD.read_text())
    baseline = json.loads(BASELINE.read_text())
    model = json.loads(MODEL.read_text())
    unit = json.loads(UNIT.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "PREDECLARED_COMPARISON_METRIC_2026_06_01"
    assert data["object"] == "PREDECLARED_COMPARISON_METRIC"
    assert data["status"] == "PREDECLARED_COMPARISON_METRIC_SUPPLIED_NO_COMPARISON_RUN_OUTPUT"
    assert data["decision"] == "PASS"

    assert auth["object"] == "AUTHENTICATED_GRAVITY_PAYLOAD"
    assert coord["object"] == "COORDINATE_OR_ROW_BINDING_CERTIFICATE"
    assert baseline["object"] == "BASELINE_GRAVITY_VECTOR"
    assert model["object"] == "MODEL_OR_DEFICIT_MASS_VECTOR"
    assert unit["object"] == "UNIT_CONVERSION_CERTIFICATE"

    metric = data["predeclared_metric"]
    assert metric["metric_id"] == "canonical_rmse_between_aligned_vectors_v1"
    assert metric["primary_metric"] == "canonical_rmse"
    assert metric["metric_direction"] == "lower_is_better"
    assert metric["canonical_unit"] == unit["unit_conversion"]["canonical_unit"]
    assert metric["vector_length"] == baseline["baseline_vector"]["length"]
    assert metric["vector_length"] == model["model_or_deficit_mass_vector"]["length"]
    assert isinstance(metric["factor_to_canonical"], (int, float))
    assert math.isfinite(float(metric["factor_to_canonical"]))
    assert float(metric["factor_to_canonical"]) > 0
    assert isinstance(metric["offset_to_canonical"], (int, float))
    assert math.isfinite(float(metric["offset_to_canonical"]))

    schema = data["required_run_output_schema"]
    assert schema["run_output_supplied"] is False
    assert "canonical_rmse" in schema["required_fields"]
    assert "run_output_sha256" in schema["required_fields"]

    assert data["resolved_missing_input"] == "predeclared_comparison_metric"
    assert set(data["remaining_missing_inputs"]) == EXPECTED_REMAINING
    assert data["remaining_missing_input_count"] == 1
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in EXPECTED_REMAINING:
        assert token in doc

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "REPRODUCIBLE_COMPARISON_RUN_OUTPUT"
    assert data["weakest_sufficient_next_input"] == "ReproducibleComparisonRunOutput"

    print("PREDECLARED_COMPARISON_METRIC_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "metric_id": metric["metric_id"],
        "primary_metric": metric["primary_metric"],
        "vector_length": metric["vector_length"],
        "resolved_missing_input": data["resolved_missing_input"],
        "remaining_missing_input_count": data["remaining_missing_input_count"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
