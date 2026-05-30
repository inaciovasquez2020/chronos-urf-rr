#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/gracefo_payload_digest_and_schema_validation_run_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/GRACEFOPayloadDigestAndSchemaValidationRun.lean")
DOC = Path("docs/status/GRACEFO_PAYLOAD_DIGEST_AND_SCHEMA_VALIDATION_RUN_2026_05_29.md")

data = json.loads(ART.read_text())
art_text = ART.read_text()
lean_text = LEAN.read_text()
doc_text = DOC.read_text()

assert data["status"] == "PAYLOAD_DIGEST_AND_SCHEMA_VALIDATION_RUN_GATE_ONLY"
assert data["dataset"]["dataset_name"] == "GRACEFO_L2_JPL_MONTHLY_0063"
assert data["digest_gate"]["algorithm"] == "SHA256"
assert data["digest_gate"]["digest_required"] is True
assert data["digest_gate"]["digest_value_supplied"] is False
assert data["schema_gate"]["schema_validation_required"] is True
assert data["schema_gate"]["schema_validation_executed"] is False

required_tokens = [
    "GRACEFO_PAYLOAD_DIGEST_AND_SCHEMA_VALIDATION_RUN_2026_05_29",
    "PAYLOAD_DIGEST_AND_SCHEMA_VALIDATION_RUN_GATE_ONLY",
    "GRACEFO_L2_JPL_MONTHLY_0063",
    "SHA256",
    "GRACEFO_L2_JPL_MONTHLY_0063_SCHEMA_V1",
    "YTR_GRAVITY_TIDAL_DERIVATIVE_REAL_DATASET_FALSIFICATION_RUN_2026_05_29",
]

missing_artifact = [token for token in required_tokens if token not in art_text]
assert not missing_artifact, f"artifact missing tokens: {missing_artifact}"

required_lean = [
    "GRACEFOPayloadDigestSpec",
    "GRACEFOSchemaValidationSpec",
    "GRACEFOPayloadDigestAndSchemaValidationRun",
    "graceFOPayloadDigestAndSchemaValidationRun_boundary_closed",
    "graceFOPayloadDigestAndSchemaValidationRun_no_overclaim",
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

print("GRACEFO_PAYLOAD_DIGEST_AND_SCHEMA_VALIDATION_RUN_OK")
