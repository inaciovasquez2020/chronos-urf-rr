#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/ytr_gravity_elastic_prediction_vector_real_data_run_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_GRAVITY_ELASTIC_PREDICTION_VECTOR_REAL_DATA_RUN_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/YtRGravityElasticPredictionVectorRealDataRun.lean"

art_text = ART.read_text()
doc_text = DOC.read_text()
lean_text = LEAN.read_text()
data = json.loads(art_text)

assert data["object"] == "YtRGravityElasticPredictionVectorRealDataRun"
assert data["status"] == "PREDICTION_VECTOR_INTERFACE_ONLY_NO_REAL_DATA_RUN_EXECUTED"
assert "YtRGravityElasticSchemaValidationRun" in art_text
assert "YtRGravityElasticSchemaValidationRun" in lean_text

for token in [
    "modelVersionFrozen",
    "predictionCodeFrozen",
    "noOutcomeLeakage",
    "realDataPredictionVectorProduced",
    "runMetadataRecorded",
]:
    assert token in art_text
    assert token in lean_text

for token in [
    "Does not prove:",
    "prediction vector executed on authentic data",
    "dark matter replacement",
    "any Clay problem",
]:
    assert token in doc_text

print("YTR_GRAVITY_ELASTIC_PREDICTION_VECTOR_REAL_DATA_RUN_OK")
