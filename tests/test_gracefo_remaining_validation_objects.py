from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/gracefo_remaining_validation_objects_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/GRACEFORemainingValidationObjects.lean")

def test_remaining_status():
    data = json.loads(ART.read_text())
    assert data["status"] == "REMAINING_GRACEFO_VALIDATION_OBJECTS_REGISTERED_AS_REQUIRED_ONLY"

def test_digest_certificate_required_only():
    digest = json.loads(ART.read_text())["objects"]["authenticated_payload_digest_certificate"]
    assert digest["name"] == "AuthenticatedGRACEFOPayloadDigestCertificate"
    assert digest["digest_algorithm"] == "SHA256"
    assert digest["digest_value"] == "UNSUPPLIED_REQUIRED_INPUT"
    assert digest["payload_bytes_supplied"] is False
    assert digest["digest_authentication_executed"] is False

def test_schema_execution_required_only():
    schema = json.loads(ART.read_text())["objects"]["schema_validation_execution_result"]
    assert schema["name"] == "GRACEFOSchemaValidationExecutionResult"
    assert schema["authenticated_digest_required"] is True
    assert schema["schema_validation_executed"] is False

def test_real_model_run_required_only():
    model = json.loads(ART.read_text())["objects"]["real_model_run"]
    assert model["name"] == "RealGRACEFOTidalDerivativeModelRun"
    assert model["model_run_executed"] is False
    assert model["empirical_result_supplied"] is False

def test_lean_surface_contains_all_objects():
    text = LEAN.read_text()
    assert "AuthenticatedGRACEFOPayloadDigestCertificate" in text
    assert "GRACEFOSchemaValidationExecutionResult" in text
    assert "RealGRACEFOTidalDerivativeModelRun" in text
    assert "GRACEFORemainingValidationObjects" in text

def test_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_gracefo_remaining_validation_objects.py"],
        check=True,
    )
