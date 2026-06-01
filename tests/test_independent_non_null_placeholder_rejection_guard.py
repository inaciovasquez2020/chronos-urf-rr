import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/independent_non_null_placeholder_rejection_guard_2026_06_01.json")
VERIFY = Path("tools/verify_independent_non_null_placeholder_rejection_guard.py")


def test_placeholder_rejection_guard_status():
    data = json.loads(ART.read_text())
    assert data["status"] == "PLACEHOLDER_REJECTION_GUARD_SUPPLIED_PAYLOAD_RESULT_NOT_SUPPLIED"
    assert data["required_input_supplied"] is False


def test_placeholder_rejection_guard_rejections_recorded():
    data = json.loads(ART.read_text())
    assert "Route A template placeholders must not validate as a real payload" in data["guarded_rejections"]
    assert "Route B template placeholders must not validate as a real payload" in data["guarded_rejections"]
    assert "Route A all-zero vectors must not validate as real non-null predictive vectors" in data["guarded_rejections"]
    assert "Route B row-unit mismatch must not validate as an external gravity payload result" in data["guarded_rejections"]


def test_placeholder_rejection_guard_boundaries():
    data = json.loads(ART.read_text())
    assert "no independent predictive DFM-MKC model supplied" in data["claim_boundaries"]
    assert "no external gravity payload result supplied" in data["claim_boundaries"]
    assert "no empirical gravity result" in data["claim_boundaries"]
    assert "no Clay problem closure" in data["claim_boundaries"]


def test_placeholder_rejection_guard_next_object():
    data = json.loads(ART.read_text())
    assert data["next_admissible_object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT"
    assert data["weakest_sufficient_next_input"] == "IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult"


def test_placeholder_rejection_guard_verifier():
    result = subprocess.run(["python3", str(VERIFY)], text=True, capture_output=True, check=True)
    assert "INDEPENDENT_NON_NULL_PLACEHOLDER_REJECTION_GUARD_OK" in result.stdout
    assert '"decision": "PASS"' in result.stdout
