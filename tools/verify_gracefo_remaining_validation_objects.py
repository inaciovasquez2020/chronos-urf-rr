#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/gracefo_remaining_validation_objects_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/GRACEFORemainingValidationObjects.lean")
DOC = Path("docs/status/GRACEFO_REMAINING_VALIDATION_OBJECTS_2026_05_29.md")

data = json.loads(ART.read_text())
art_text = ART.read_text()
lean_text = LEAN.read_text()
doc_text = DOC.read_text()

assert data["status"] == "REMAINING_GRACEFO_VALIDATION_OBJECTS_REGISTERED_AS_REQUIRED_ONLY"
assert data["successor_to"] == "GRACEFO_PAYLOAD_DIGEST_AND_SCHEMA_VALIDATION_RUN_2026_05_29"
assert data["weakest_missing_input"] == "actual_GRACEFO_payload_bytes_and_SHA256_digest"

digest = data["objects"]["authenticated_payload_digest_certificate"]
schema = data["objects"]["schema_validation_execution_result"]
model = data["objects"]["real_model_run"]

assert digest["name"] == "AuthenticatedGRACEFOPayloadDigestCertificate"
assert digest["digest_algorithm"] == "SHA256"
assert digest["payload_bytes_supplied"] is False
assert digest["digest_value_supplied"] is False
assert digest["digest_authentication_executed"] is False

assert schema["name"] == "GRACEFOSchemaValidationExecutionResult"
assert schema["authenticated_digest_required"] is True
assert schema["schema_validation_executed"] is False
assert schema["schema_validation_passed"] is False

assert model["name"] == "RealGRACEFOTidalDerivativeModelRun"
assert model["observable"] == "radial_gravity_gradient_dg_dr"
assert model["baseline"] == "standard_GR_or_Newtonian_geodesy_prediction"
assert model["model_run_executed"] is False
assert model["empirical_result_supplied"] is False

required_lean = [
    "AuthenticatedGRACEFOPayloadDigestCertificate",
    "GRACEFOSchemaValidationExecutionResult",
    "RealGRACEFOTidalDerivativeModelRun",
    "GRACEFORemainingValidationObjects",
    "authenticatedGRACEFOPayloadDigestCertificate_boundary_closed",
    "graceFOSchemaValidationExecutionResult_boundary_closed",
    "realGRACEFOTidalDerivativeModelRun_boundary_closed",
    "graceFORemainingValidationObjects_boundary_closed",
]

missing_lean = [token for token in required_lean if token not in lean_text]
assert not missing_lean, f"Lean missing tokens: {missing_lean}"

for forbidden in [
    "GR failure proved",
    "new gravity proved",
    "dark matter replaced",
    "Lambda-CDM failure proved",
    "quantum gravity proved",
    "Clay problem solved",
]:
    assert forbidden not in art_text
    assert forbidden not in lean_text
    assert forbidden not in doc_text

print("GRACEFO_REMAINING_VALIDATION_OBJECTS_OK")
