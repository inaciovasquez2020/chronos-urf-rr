#!/usr/bin/env python3
import json
import math
from pathlib import Path

ART = Path("artifacts/chronos/unit_conversion_certificate_2026_06_01.json")
DOC = Path("docs/status/UNIT_CONVERSION_CERTIFICATE_2026_06_01.md")
BASELINE = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")
MODEL = Path("artifacts/chronos/model_or_deficit_mass_vector_2026_06_01.json")
COORD = Path("artifacts/chronos/coordinate_or_row_binding_certificate_2026_06_01.json")
AUTH = Path("artifacts/chronos/authenticated_gravity_payload_2026_06_01.json")

EXPECTED_REMAINING = {
    "predeclared_comparison_metric",
    "reproducible_comparison_run_output",
}

REQUIRED_NON_CLAIMS = {
    "unit conversion certificate only",
    "no predeclared comparison metric supplied",
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
    "PREDECLARED_COMPARISON_METRIC_SUPPLIED_TRUE",
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
    assert BASELINE.exists(), f"missing baseline artifact: {BASELINE}"
    assert MODEL.exists(), f"missing model artifact: {MODEL}"
    assert COORD.exists(), f"missing coordinate artifact: {COORD}"
    assert AUTH.exists(), f"missing authenticated payload artifact: {AUTH}"

    data = json.loads(ART.read_text())
    baseline = json.loads(BASELINE.read_text())
    model = json.loads(MODEL.read_text())
    coord = json.loads(COORD.read_text())
    auth = json.loads(AUTH.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "UNIT_CONVERSION_CERTIFICATE_2026_06_01"
    assert data["object"] == "UNIT_CONVERSION_CERTIFICATE"
    assert data["status"] == "UNIT_CONVERSION_CERTIFICATE_SUPPLIED_FOR_BASELINE_AND_MODEL_VECTOR_ALIGNMENT"
    assert data["decision"] == "PASS"

    assert baseline["object"] == "BASELINE_GRAVITY_VECTOR"
    assert model["object"] == "MODEL_OR_DEFICIT_MASS_VECTOR"
    assert coord["object"] == "COORDINATE_OR_ROW_BINDING_CERTIFICATE"
    assert auth["object"] == "AUTHENTICATED_GRAVITY_PAYLOAD"

    assert data["source_payload"]["sha256"] == auth["sha256"]
    assert data["source_baseline_vector"]["baseline_vector_sha256"] == baseline["baseline_vector"]["sha256"]
    assert data["source_model_or_deficit_mass_vector"]["vector_sha256"] == model["model_or_deficit_mass_vector"]["sha256"]

    conv = data["unit_conversion"]
    assert conv["source_units_raw"]
    assert conv["source_units_normalized"]
    assert conv["canonical_unit"] == "meter liquid-water-equivalent thickness"
    assert isinstance(conv["factor_to_canonical"], (int, float))
    assert isinstance(conv["offset_to_canonical"], (int, float))
    assert math.isfinite(float(conv["factor_to_canonical"]))
    assert math.isfinite(float(conv["offset_to_canonical"]))
    assert float(conv["factor_to_canonical"]) > 0

    assert data["vector_alignment_check"]["same_length"] is True
    assert data["vector_alignment_check"]["baseline_vector_length"] == baseline["baseline_vector"]["length"]
    assert data["vector_alignment_check"]["model_or_deficit_mass_vector_length"] == model["model_or_deficit_mass_vector"]["length"]

    assert data["resolved_missing_input"] == "unit_conversion_certificate"
    assert set(data["remaining_missing_inputs"]) == EXPECTED_REMAINING
    assert data["remaining_missing_input_count"] == 2
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in EXPECTED_REMAINING:
        assert token in doc

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "PREDECLARED_COMPARISON_METRIC"
    assert data["weakest_sufficient_next_input"] == "PredeclaredComparisonMetric"

    print("UNIT_CONVERSION_CERTIFICATE_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "source_units_raw": conv["source_units_raw"],
        "canonical_unit": conv["canonical_unit"],
        "factor_to_canonical": conv["factor_to_canonical"],
        "resolved_missing_input": data["resolved_missing_input"],
        "remaining_missing_input_count": data["remaining_missing_input_count"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
