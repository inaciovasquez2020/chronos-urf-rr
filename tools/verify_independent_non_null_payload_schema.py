#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ART = Path("artifacts/chronos/independent_non_null_payload_schema_2026_06_01.json")
PY_SCHEMA = Path("schemas/chronos/independent_non_null_payload_schema.py")
TS_SCHEMA = Path("schemas/chronos/independent_non_null_payload_schema.ts")

data = json.loads(ART.read_text())
assert data["object"] == "INDEPENDENT_NON_NULL_PAYLOAD_SCHEMA"
assert data["decision"] == "PASS"
assert data["status"] == "SCHEMA_CLOSED_PAYLOAD_RESULT_NOT_SUPPLIED"
assert data["required_input_supplied"] is False
assert data["schema_version"] == "2026-06-01.v1"
assert data["next_admissible_object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT"
assert data["weakest_sufficient_next_input"] == "IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult"

py_text = PY_SCHEMA.read_text()
ts_text = TS_SCHEMA.read_text()

for required in [
    "at least one value must be nonzero",
    "independence_certificate_sha256",
    "canonical_json",
    "payload_from_dict",
    "required_input_supplied",
]:
    assert required in py_text

for required in [
    "Number.isFinite",
    "at least one value must be nonzero",
    "independence_certificate_sha256",
    "requiredInputSupplied",
    "SCHEMA_VERSION",
]:
    assert required in ts_text

spec = importlib.util.spec_from_file_location("independent_non_null_payload_schema", PY_SCHEMA)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

route_a = mod.make_route_a_stub()
route_b = mod.make_route_b_stub()
mod.validate_payload(route_a)
mod.validate_payload(route_b)
assert mod.required_input_supplied(route_a) is True
assert mod.required_input_supplied(route_b) is True
assert mod.payload_from_dict(mod.payload_to_dict(route_a)) == route_a
assert mod.payload_from_dict(mod.payload_to_dict(route_b)) == route_b

try:
    bad_a = mod.IndependentNonNullPredictiveModelVector(
        metadata=route_a.metadata,
        coordinates=route_a.coordinates,
        values=[0.0 for _ in route_a.values],
        unit=route_a.unit,
    )
    mod.validate_payload(bad_a)
    raise AssertionError("all-zero Route A vector unexpectedly validated")
except ValueError as exc:
    assert "nonzero" in str(exc)

subprocess.run(["python3", str(PY_SCHEMA)], check=True, text=True, capture_output=True)

print("INDEPENDENT_NON_NULL_PAYLOAD_SCHEMA_OK")
print(json.dumps({
    "artifact": str(ART),
    "decision": data["decision"],
    "status": data["status"],
    "schema_version": data["schema_version"],
    "required_input_supplied": data["required_input_supplied"],
    "next_admissible_object": data["next_admissible_object"],
}, indent=2, sort_keys=True))
