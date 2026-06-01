#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/independent_non_null_predictive_model_vector_or_external_gravity_payload_result_target_2026_06_01.json")
SRC = Path("artifacts/chronos/non_null_model_result_interpretation_2026_06_01.json")

data = json.loads(ART.read_text())
src = json.loads(SRC.read_text())

assert data["object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT_TARGET"
assert data["decision"] == "PASS"
assert data["status"] == "TARGET_OPEN_INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT_NOT_SUPPLIED"
assert data["source_interpretation_artifact"] == str(SRC)
assert data["source_interpretation_status"] == src["status"]
assert data["source_result_class"] == src["result_class"]
assert data["source_favored_result"] == src["favored_result"]
assert data["required_input_supplied"] is False
assert data["accepted_input_shapes"] == [
    "independent_non_null_predictive_model_vector",
    "external_gravity_payload_result",
]
assert data["missing_inputs"] == [
    "independent_non_null_predictive_model_vector",
    "external_gravity_payload_result",
]
assert "no independent predictive non-null model vector supplied" in data["blocked_by"]
assert "no external gravity payload result supplied" in data["blocked_by"]
assert data["next_admissible_object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT"
assert data["weakest_sufficient_next_input"] == "IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult"

for forbidden in [
    "no independent predictive DFM-MKC model supplied",
    "no external gravity payload result supplied",
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

print("INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT_TARGET_OK")
print(json.dumps({
    "artifact": str(ART),
    "decision": data["decision"],
    "status": data["status"],
    "required_input_supplied": data["required_input_supplied"],
    "next_admissible_object": data["next_admissible_object"],
}, indent=2, sort_keys=True))
