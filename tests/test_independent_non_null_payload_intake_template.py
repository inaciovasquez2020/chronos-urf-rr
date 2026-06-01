import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/independent_non_null_payload_intake_template_2026_06_01.json")
VERIFY = Path("tools/verify_independent_non_null_payload_intake_template.py")


def test_intake_template_artifact_status():
    data = json.loads(ART.read_text())
    assert data["status"] == "INTAKE_TEMPLATE_SUPPLIED_PAYLOAD_RESULT_NOT_SUPPLIED"
    assert data["required_input_supplied"] is False


def test_route_a_template_shape():
    data = json.loads(ART.read_text())
    route_a = json.loads(Path(data["route_a_template"]).read_text())
    assert route_a["schema_version"] == "2026-06-01.v1"
    assert route_a["route"] == "A"
    assert route_a["metadata"]["independent_of_lwe_baseline"] is True
    assert len(route_a["coordinates"]) == len(route_a["values"])


def test_route_b_template_shape():
    data = json.loads(ART.read_text())
    route_b = json.loads(Path(data["route_b_template"]).read_text())
    assert route_b["schema_version"] == "2026-06-01.v1"
    assert route_b["route"] == "B"
    assert route_b["rows"][0]["unit"] == route_b["unit"]
    assert len(route_b["comparison_metrics"]) >= 1


def test_intake_template_boundaries():
    data = json.loads(ART.read_text())
    assert "no independent predictive DFM-MKC model supplied" in data["claim_boundaries"]
    assert "no external gravity payload result supplied" in data["claim_boundaries"]
    assert "no empirical gravity result" in data["claim_boundaries"]
    assert "no Clay problem closure" in data["claim_boundaries"]


def test_intake_template_verifier():
    result = subprocess.run(["python3", str(VERIFY)], text=True, capture_output=True, check=True)
    assert "INDEPENDENT_NON_NULL_PAYLOAD_INTAKE_TEMPLATE_OK" in result.stdout
    assert '"decision": "PASS"' in result.stdout
