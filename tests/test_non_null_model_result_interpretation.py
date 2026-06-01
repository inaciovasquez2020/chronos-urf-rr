import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/non_null_model_result_interpretation_2026_06_01.json")
VERIFY = Path("tools/verify_non_null_model_result_interpretation.py")

def test_non_null_model_result_interpretation_artifact_exists():
    assert ART.exists()

def test_non_null_model_result_interpretation_status_and_boundary():
    data = json.loads(ART.read_text())
    assert data["status"] == "NON_NULL_MODEL_RESULT_INTERPRETED_NO_EMPIRICAL_OR_PHYSICAL_CLAIM"
    assert data["result_class"] == "derived_baseline_identity_residual_recorded"
    assert data["favored_result"] == "none"
    assert "no empirical gravity result" in data["claim_boundaries"]
    assert "no model-favored result claim" in data["claim_boundaries"]

def test_non_null_model_result_interpretation_metric_binding():
    data = json.loads(ART.read_text())
    assert data["primary_metric"] == "canonical_mae"
    assert data["primary_metric_value"] == data["canonical_mae"]
    assert data["canonical_mae"] == 4.093452153728917e-18
    assert data["canonical_rmse"] == 4.707946048927731e-17

def test_non_null_model_result_interpretation_next_object():
    data = json.loads(ART.read_text())
    assert data["next_admissible_object"] == "INDEPENDENT_NON_NULL_PREDICTIVE_MODEL_VECTOR_OR_EXTERNAL_GRAVITY_PAYLOAD_RESULT"
    assert data["weakest_sufficient_next_input"] == "IndependentNonNullPredictiveModelVectorOrExternalGravityPayloadResult"

def test_non_null_model_result_interpretation_verifier():
    result = subprocess.run(["python3", str(VERIFY)], text=True, capture_output=True, check=True)
    assert "NON_NULL_MODEL_RESULT_INTERPRETATION_OK" in result.stdout
    assert '"decision": "PASS"' in result.stdout
