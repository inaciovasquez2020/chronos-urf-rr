import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
ART = Path("artifacts/chronos/independent_non_null_payload_result_intake_gate_2026_06_01.json")
RUNNER = Path("tools/intake_independent_non_null_payload_result.py")
SCHEMA = Path("schemas/chronos/independent_non_null_payload_schema.py")
VERIFY = Path("tools/verify_independent_non_null_payload_result_intake_gate.py")
def load_schema():
spec = importlib.util.spec_from_file_location("independent_non_null_payload_schema", SCHEMA)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
return mod
def test_intake_gate_artifact_status():
data = json.loads(ART.read_text())
assert data["status"] == "INTAKE_GATE_SUPPLIED_PAYLOAD_RESULT_NOT_SUPPLIED"
assert data["required_input_supplied"] is False
assert data["accepted_routes"] == ["A", "B"]
def test_route_a_payload_ingests():
mod = load_schema()
with tempfile.TemporaryDirectory() as tmp:
tmpdir = Path(tmp)
payload = tmpdir / "route_a.json"
out = tmpdir / "out.json"
payload.write_text(json.dumps(mod.payload_to_dict(mod.make_route_a_stub()), indent=2, sort_keys=True))
result = subprocess.run(["python3", str(RUNNER), str(payload), "--out", str(out)], text=True, capture_output=True, check=True)
assert "INDEPENDENT_NON_NULL_PAYLOAD_RESULT_INGESTED" in result.stdout
ingested = json.loads(out.read_text())
assert ingested["route"] == "A"
assert ingested["required_input_supplied"] is True
def test_route_b_payload_ingests():
mod = load_schema()
with tempfile.TemporaryDirectory() as tmp:
tmpdir = Path(tmp)
payload = tmpdir / "route_b.json"
out = tmpdir / "out.json"
payload.write_text(json.dumps(mod.payload_to_dict(mod.make_route_b_stub()), indent=2, sort_keys=True))
result = subprocess.run(["python3", str(RUNNER), str(payload), "--out", str(out)], text=True, capture_output=True, check=True)
assert "INDEPENDENT_NON_NULL_PAYLOAD_RESULT_INGESTED" in result.stdout
ingested = json.loads(out.read_text())
assert ingested["route"] == "B"
assert ingested["required_input_supplied"] is True
def test_intake_gate_boundaries():
data = json.loads(ART.read_text())
assert "no independent predictive DFM-MKC model supplied" in data["claim_boundaries"]
assert "no external gravity payload result supplied" in data["claim_boundaries"]
assert "no empirical gravity result" in data["claim_boundaries"]
assert "no Clay problem closure" in data["claim_boundaries"]
def test_intake_gate_verifier():
result = subprocess.run(["python3", str(VERIFY)], text=True, capture_output=True, check=True)
assert "INDEPENDENT_NON_NULL_PAYLOAD_RESULT_INTAKE_GATE_OK" in result.stdout
assert '"decision": "PASS"' in result.stdout
