#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
ART_DIR = ROOT / "artifacts/sparc/rotation_curve_step3_5_2026_05_28"
DOC = ROOT / "docs/status/SPARC_ROTATION_CURVE_STEP3_5_ACCOUNTING_RUN_AND_PREDICTIVE_TARGET_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/SparcRotationCurveStep35AccountingRun.lean"
RECORD = ART_DIR / "SPARC_ROTATION_CURVE_STEP3_5_ACCOUNTING_RUN_AND_PREDICTIVE_TARGET_2026_05_28.json"
REQUIRED = ["SPARC_STEP3_5_COMPLETION_SUMMARY_2026_05_28.txt","BARYONIC_VELOCITY_CONVENTION_FOR_SPARC_2026_05_28.txt","BASELINE_MODEL_PREDICTION_VECTOR_2026_05_28.csv","DEFICIT_MASS_MODEL_PREDICTION_VECTOR_2026_05_28.csv","LIKELIHOOD_COMPARISON_RESULT_2026_05_28.json","LIKELIHOOD_COMPARISON_PER_GALAXY_2026_05_28.csv","SPARC_STEP3_5_PREDICTION_LIKELIHOOD_ARTIFACTS_2026_05_28.zip","SPARC_ROTATION_CURVE_STEP3_5_ACCOUNTING_RUN_AND_PREDICTIVE_TARGET_2026_05_28.json"]
TOKENS = ["PredictiveDeficitMassLawOrLowParameterDeficitMassModel","SATURATED_ACCOUNTING_RUN_ARCHIVED_PREDICTIVE_DEFICIT_MODEL_TARGET_OPEN","No predictive GDM law closure","No low-parameter deficit-mass model closure","No dark matter replacement claim","No Lambda-CDM failure claim","No PhD-complete final result claim","No unrestricted Chronos-RR","No unrestricted H4.1/FGL","No P vs NP","No Clay problem"]
def fail(msg: str):
    print(f"SPARC_STEP3_5_ACCOUNTING_RUN_VERIFY_FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)
for name in REQUIRED:
    if not (ART_DIR / name).exists(): fail(f"missing artifact {name}")
if not DOC.exists(): fail("missing status doc")
if not LEAN.exists(): fail("missing Lean module")
record = json.loads(RECORD.read_text())
if record.get("formal_status") != "SATURATED_ACCOUNTING_RUN_ARCHIVED_PREDICTIVE_DEFICIT_MODEL_TARGET_OPEN": fail("wrong formal_status")
if record.get("open_object") != "PredictiveDeficitMassLawOrLowParameterDeficitMassModel": fail("wrong open object")
metrics = record.get("metrics", {})
expected = {"chi2_baseline": 1960466.562888448,"chi2_gdm_saturated_accounting": 4511.003922882878,"delta_chi2_gdm_minus_baseline": -1955955.558965565,"positive_deficit_rows": 3177}
for key, value in expected.items():
    got = metrics.get(key)
    if got is None or abs(got - value) > 1e-6: fail(f"metric mismatch {key}: {got!r} != {value!r}")
combined = DOC.read_text() + "\n" + LEAN.read_text() + "\n" + RECORD.read_text()
for token in TOKENS:
    if token not in combined: fail(f"missing token {token}")
print("SPARC_STEP3_5_ACCOUNTING_RUN_AND_PREDICTIVE_TARGET_OK")
