#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/ytr_gravity_elastic_schema_validation_run_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_GRAVITY_ELASTIC_SCHEMA_VALIDATION_RUN_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/YtRGravityElasticSchemaValidationRun.lean"

art_text = ART.read_text()
doc_text = DOC.read_text()
lean_text = LEAN.read_text()
data = json.loads(art_text)

assert data["object"] == "YtRGravityElasticSchemaValidationRun"
assert data["status"] == "SCHEMA_VALIDATION_INTERFACE_ONLY_NO_REAL_SCHEMA_RUN_EXECUTED"
assert "AuthenticYtRGravityElasticDatasetPayloadBinding" in art_text
assert "AuthenticYtRGravityElasticDatasetPayloadBinding" in lean_text

for token in [
    "schemaDeclared",
    "requiredFieldsPresent",
    "unitsValidated",
    "finiteRowsValidated",
    "missingnessPolicyRecorded",
]:
    assert token in art_text
    assert token in lean_text

for token in [
    "Does not prove:",
    "schema validation executed on authentic payload",
    "unrestricted H4.1/FGL",
    "any Clay problem",
]:
    assert token in doc_text

print("YTR_GRAVITY_ELASTIC_SCHEMA_VALIDATION_RUN_OK")
