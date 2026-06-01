#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ART = Path("artifacts/chronos/independent_non_null_placeholder_rejection_guard_2026_06_01.json")
SCHEMA = Path("schemas/chronos/independent_non_null_payload_schema.py")
RUNNER = Path("tools/intake_independent_non_null_payload_result.py")

data = json.loads(ART.read_text())

assert data["object"] == "INDEPENDENT_NON_NULL_PLACEHOLDER_REJECTION_GUARD"
assert data["decision"] == "PASS"
assert data["status"] == "PLACEHOLDER_REJECTION_GUARD_SUPPLIED_PAYLOAD_RESULT_NOT_SUPPLIED"
assert data["required_input_supplied"] is False
assert data["schema"] == str(SCHEMA)
assert data["runner"] == str(RUNNER)
assert data["next_admissible_object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT"
assert data["weakest_sufficient_next_input"] == "IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult"

for item in [
    "Route A template placeholders must not validate as a real payload",
    "Route B template placeholders must not validate as a real payload",
    "Route A all-zero vectors must not validate as real non-null predictive vectors",
    "Route B row-unit mismatch must not validate as an external gravity payload result",
]:
    assert item in data["guarded_rejections"]

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

def assert_runner_rejects(payload_path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out.json"
        result = subprocess.run(
            ["python3", str(RUNNER), str(payload_path), "--out", str(out)],
            text=True,
            capture_output=True,
        )
        assert result.returncode != 0
        assert not out.exists()

route_a_template = Path(data["route_a_template"])
route_b_template = Path(data["route_b_template"])
assert_runner_rejects(route_a_template)
assert_runner_rejects(route_b_template)

with tempfile.TemporaryDirectory() as tmp:
    tmpdir = Path(tmp)

    zero_payload = tmpdir / "route_a_zero.json"
    route_a = mod.payload_to_dict(mod.make_route_a_stub())
    route_a["values"] = [0.0 for _ in route_a["values"]]
    zero_payload.write_text(json.dumps(route_a, indent=2, sort_keys=True) + "\n")
    assert_runner_rejects(zero_payload)

    mismatch_payload = tmpdir / "route_b_unit_mismatch.json"
    route_b = mod.payload_to_dict(mod.make_route_b_stub())
    route_b["rows"][0]["unit"] = "kg_m2"
    mismatch_payload.write_text(json.dumps(route_b, indent=2, sort_keys=True) + "\n")
    assert_runner_rejects(mismatch_payload)

print("INDEPENDENT_NON_NULL_PLACEHOLDER_REJECTION_GUARD_OK")
print(json.dumps({
    "artifact": str(ART),
    "decision": data["decision"],
    "status": data["status"],
    "required_input_supplied": data["required_input_supplied"],
    "guarded_rejection_count": len(data["guarded_rejections"]),
    "next_admissible_object": data["next_admissible_object"],
}, indent=2, sort_keys=True))
