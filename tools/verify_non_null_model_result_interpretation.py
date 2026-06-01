#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/non_null_model_result_interpretation_2026_06_01.json")
SRC = Path("artifacts/chronos/non_null_model_comparison_run_output_2026_06_01.json")

data = json.loads(ART.read_text())
src = json.loads(SRC.read_text())

assert data["object"] == "NON_NULL_MODEL_RESULT_INTERPRETATION"
assert data["decision"] == "PASS"
assert data["status"] == "NON_NULL_MODEL_RESULT_INTERPRETED_NO_EMPIRICAL_OR_PHYSICAL_CLAIM"
assert data["source_run_output"] == str(SRC)
assert data["source_run_output_sha256"] == src["run_output_sha256"]
assert data["canonical_mae"] == src["canonical_mae"]
assert data["canonical_rmse"] == src["canonical_rmse"]
assert data["canonical_max_abs_error"] == src["canonical_max_abs_error"]
assert data["canonical_mean_signed_error"] == src["canonical_mean_signed_error"]
assert data["primary_metric"] == "canonical_mae"
assert data["primary_metric_value"] == src["canonical_mae"]
assert data["result_class"] == "derived_baseline_identity_residual_recorded"
assert data["favored_result"] == "none"
assert data["remaining_missing_input_count"] == 0
assert data["next_admissible_object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT"
assert data["weakest_sufficient_next_input"] == "IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult"

for forbidden in [
    "no empirical gravity result",
    "no anomaly detection claim",
    "no model-favored result claim",
    "no DFM-MKC validation",
    "no Lambda-CDM failure",
    "no physical discovery",
    "no Chronos-RR closure",
    "no P vs NP closure",
    "no Clay problem closure",
]:
    assert forbidden in data["claim_boundaries"]

print("NON_NULL_MODEL_RESULT_INTERPRETATION_OK")
print(json.dumps({
    "artifact": str(ART),
    "decision": data["decision"],
    "status": data["status"],
    "result_class": data["result_class"],
    "favored_result": data["favored_result"],
    "primary_metric_value": data["primary_metric_value"],
    "next_admissible_object": data["next_admissible_object"],
}, indent=2, sort_keys=True))
