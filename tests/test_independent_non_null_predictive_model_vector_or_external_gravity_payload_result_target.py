import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/independent_non_null_predictive_model_vector_or_external_gravity_payload_result_target_2026_06_01.json")
VERIFY = Path("tools/verify_independent_non_null_predictive_model_vector_or_external_gravity_payload_result_target.py")

def test_independent_non_null_target_artifact_exists():
    assert ART.exists()

def test_independent_non_null_target_status():
    data = json.loads(ART.read_text())
    assert data["status"] == "TARGET_OPEN_INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT_NOT_SUPPLIED"
    assert data["required_input_supplied"] is False

def test_independent_non_null_target_missing_inputs():
    data = json.loads(ART.read_text())
    assert data["missing_inputs"] == [
        "independent_non_null_predictive_model_vector",
        "external_gravity_payload_result",
    ]

def test_independent_non_null_target_boundaries():
    data = json.loads(ART.read_text())
    assert "no independent predictive DFM-MKC model supplied" in data["claim_boundaries"]
    assert "no external gravity payload result supplied" in data["claim_boundaries"]
    assert "no empirical gravity result" in data["claim_boundaries"]
    assert "no Clay problem closure" in data["claim_boundaries"]

def test_independent_non_null_target_next_object():
    data = json.loads(ART.read_text())
    assert data["next_admissible_object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT"
    assert data["weakest_sufficient_next_input"] == "IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult"

def test_independent_non_null_target_verifier():
    result = subprocess.run(["python3", str(VERIFY)], text=True, capture_output=True, check=True)
    assert "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT_TARGET_OK" in result.stdout
    assert '"decision": "PASS"' in result.stdout
