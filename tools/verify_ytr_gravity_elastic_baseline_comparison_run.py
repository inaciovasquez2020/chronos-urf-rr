#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/ytr_gravity_elastic_baseline_comparison_run_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_GRAVITY_ELASTIC_BASELINE_COMPARISON_RUN_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/YtRGravityElasticBaselineComparisonRun.lean"

art_text = ART.read_text()
doc_text = DOC.read_text()
lean_text = LEAN.read_text()
data = json.loads(art_text)

assert data["object"] == "YtRGravityElasticBaselineComparisonRun"
assert data["status"] == "BASELINE_COMPARISON_INTERFACE_ONLY_NO_EMPIRICAL_COMPARISON_EXECUTED"
assert "YtRGravityElasticPredictionVectorRealDataRun" in art_text
assert "YtRGravityElasticPredictionVectorRealDataRun" in lean_text

for token in [
    "standardGRComparisonExecuted",
    "lambdaCDMComparisonExecuted",
    "commonMetricDeclared",
    "baselineMetricsRecorded",
    "comparisonResultFrozen",
    "uncertaintyInputsRecorded",
]:
    assert token in art_text
    assert token in lean_text

for token in [
    "Does not prove:",
    "standard GR failure",
    "Lambda-CDM failure",
    "any Clay problem",
]:
    assert token in doc_text

print("YTR_GRAVITY_ELASTIC_BASELINE_COMPARISON_RUN_OK")
