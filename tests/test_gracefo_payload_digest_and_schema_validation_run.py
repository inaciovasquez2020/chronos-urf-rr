from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/gracefo_payload_digest_and_schema_validation_run_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/GRACEFOPayloadDigestAndSchemaValidationRun.lean")

def test_artifact_status(): assert json.loads(ART.read_text())["status"] == "PAYLOAD_DIGEST_AND_SCHEMA_VALIDATION_RUN_GATE_ONLY"

def test_dataset_binding(): assert json.loads(ART.read_text())["dataset"]["dataset_name"] == "GRACEFO_L2_JPL_MONTHLY_0063"

def test_digest_gate_requires_sha256_without_digest_value(): assert json.loads(ART.read_text())["digest_gate"] == {"algorithm": "SHA256", "digest_required": True, "digest_value_supplied": False, "payload_bytes_embedded": False}

def test_schema_gate_required_not_executed(): assert json.loads(ART.read_text())["schema_gate"]["schema_validation_required"] is True and json.loads(ART.read_text())["schema_gate"]["schema_validation_executed"] is False

def test_lean_surface_contains_run_object(): assert "GRACEFOPayloadDigestAndSchemaValidationRun" in LEAN.read_text()

def test_verifier_passes(): subprocess.run(["python3", "tools/verify_gracefo_payload_digest_and_schema_validation_run.py"], check=True)
