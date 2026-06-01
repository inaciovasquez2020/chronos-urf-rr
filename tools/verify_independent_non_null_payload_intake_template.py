#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/independent_non_null_payload_intake_template_2026_06_01.json")

data = json.loads(ART.read_text())
route_a = Path(data["route_a_template"])
route_b = Path(data["route_b_template"])
a = json.loads(route_a.read_text())
b = json.loads(route_b.read_text())

assert data["object"] == "INDEPENDENT_NON_NULL_PAYLOAD_INTAKE_TEMPLATE"
assert data["decision"] == "PASS"
assert data["status"] == "INTAKE_TEMPLATE_SUPPLIED_PAYLOAD_RESULT_NOT_SUPPLIED"
assert data["schema_version"] == "2026-06-01.v1"
assert data["required_input_supplied"] is False
assert data["template_placeholders_present"] is True
assert data["accepted_routes"] == ["A", "B"]

assert a["schema_version"] == data["schema_version"]
assert a["route"] == "A"
assert a["metadata"]["independent_of_lwe_baseline"] is True
assert len(a["coordinates"]) == len(a["values"]) == 1
assert any(v != 0.0 for v in a["values"])
assert "REPLACE_WITH_" in json.dumps(a)

assert b["schema_version"] == data["schema_version"]
assert b["route"] == "B"
assert len(b["rows"]) == 1
assert len(b["comparison_metrics"]) == 1
assert b["rows"][0]["unit"] == b["unit"]
assert "REPLACE_WITH_" in json.dumps(b)

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

assert data["next_admissible_object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT"
assert data["weakest_sufficient_next_input"] == "IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult"

print("INDEPENDENT_NON_NULL_PAYLOAD_INTAKE_TEMPLATE_OK")
print(json.dumps({
    "artifact": str(ART),
    "decision": data["decision"],
    "status": data["status"],
    "required_input_supplied": data["required_input_supplied"],
    "next_admissible_object": data["next_admissible_object"],
}, indent=2, sort_keys=True))
