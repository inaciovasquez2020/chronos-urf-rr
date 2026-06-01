#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ART = Path("artifacts/chronos/independent_non_null_payload_result_intake_gate_2026_06_01.json")
RUNNER = Path("tools/intake_independent_non_null_payload_result.py")
SCHEMA = Path("schemas/chronos/independent_non_null_payload_schema.py")

data = json.loads(ART.read_text())

assert data["object"] == "INDEPENDENT_NON_NULL_PAYLOAD_RESULT_INTAKE_GATE"
assert data["decision"] == "PASS"
assert data["status"] == "INTAKE_GATE_SUPPLIED_PAYLOAD_RESULT_NOT_SUPPLIED"
assert data["runner"] == str(RUNNER)
assert data["schema"] == str(SCHEMA)
assert data["required_input_supplied"] is False
assert data["accepted_routes"] == ["A", "B"]
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

spec = importlib.util.spec_from_file_location("independent_non_null_payload_schema", SCHEMA)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

with tempfile.TemporaryDirectory() as tmp:
    tmpdir = Path(tmp)
    payload = tmpdir / "route_a_payload.json"
    out = tmpdir / "ingested.json"

    payload.write_text(
        json.dumps(mod.payload_to_dict(mod.make_route_a_stub()), indent=2, sort_keys=True) + "\n"
    )

    result = subprocess.run(
        ["python3", str(RUNNER), str(payload), "--out", str(out)],
        text=True,
        capture_output=True,
        check=True,
    )

    assert "INDEPENDENT_NON_NULL_PAYLOAD_RESULT_INGESTED" in result.stdout
    ingested = json.loads(out.read_text())
    assert ingested["decision"] == "PASS"
    assert ingested["route"] == "A"
    assert ingested["required_input_supplied"] is True
    assert ingested["object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT"

print("INDEPENDENT_NON_NULL_PAYLOAD_RESULT_INTAKE_GATE_OK")
print(json.dumps({
    "artifact": str(ART),
    "decision": data["decision"],
    "status": data["status"],
    "runner": data["runner"],
    "required_input_supplied": data["required_input_supplied"],
    "next_admissible_object": data["next_admissible_object"],
}, indent=2, sort_keys=True))
