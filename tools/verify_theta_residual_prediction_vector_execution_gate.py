#!/usr/bin/env python3
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/ThetaResidualPredictionVectorExecutionGate.lean"
ART = ROOT / "artifacts/sparc/theta_residual_prediction_vector_execution_gate_2026_05_29.json"
CSV_PATH = ROOT / "artifacts/sparc/theta_residual_prediction_vector_execution_gate_2026_05_29.csv"
DOC = ROOT / "docs/status/THETA_RESIDUAL_PREDICTION_VECTOR_EXECUTION_GATE_2026_05_29.md"
CHRONOS = ROOT / "lean/Chronos.lean"

for path in [LEAN, ART, CSV_PATH, DOC, CHRONOS]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = LEAN.read_text()
doc_text = DOC.read_text()
chronos_text = CHRONOS.read_text()
artifact = json.loads(ART.read_text())

for token in [
    "ThetaResidualPredictionVectorExecutionGate",
    "thetaNumericRow1_prediction_numerator",
    "thetaNumericRow2_prediction_numerator",
    "thetaNumericRow3_prediction_numerator",
    "thetaExecutionGateV1_improves_fixture",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in [
    "FINITE_NUMERIC_FIXTURE_EXECUTED_NO_EMPIRICAL_VALIDATION",
    "theta_squared_error_numerator = 3300",
    "baseline_squared_error_numerator = 12000",
    "improvement_numerator = 8700",
    "AuthenticSPARCThetaResidualPredictionVectorRun",
]:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

if artifact["status"] != "FINITE_NUMERIC_FIXTURE_EXECUTED_NO_EMPIRICAL_VALIDATION":
    raise SystemExit("unexpected status")
if artifact["row_count"] != 3:
    raise SystemExit("unexpected row_count")
if artifact["next_missing_object"] != "AuthenticSPARCThetaResidualPredictionVectorRun":
    raise SystemExit("unexpected next missing object")

theta_num = artifact["theta"]["numerator"]
theta_den = artifact["theta"]["denominator"]

if theta_num != 1:
    raise SystemExit("unexpected theta numerator")
if theta_den != 2:
    raise SystemExit("unexpected theta denominator")

with CSV_PATH.open(newline="") as handle:
    rows = [
        {key: int(value) for key, value in row.items()}
        for row in csv.DictReader(handle)
    ]

if len(rows) != 3:
    raise SystemExit("expected exactly 3 rows")

theta_total = 0
baseline_total = 0

for row in rows:
    obs = row["observed_velocity_squared"]
    bary = row["baryonic_velocity_squared"]
    residual = max(obs - bary, 0)
    deficit_num = theta_num * residual
    prediction_num = theta_den * bary + deficit_num
    observed_num = theta_den * obs
    baseline_num = theta_den * bary
    theta_err = (observed_num - prediction_num) ** 2
    baseline_err = (observed_num - baseline_num) ** 2

    expected = {
        "theta_numerator": theta_num,
        "theta_denominator": theta_den,
        "residual": residual,
        "deficit_numerator": deficit_num,
        "prediction_numerator": prediction_num,
        "observed_numerator": observed_num,
        "baseline_numerator": baseline_num,
        "theta_squared_error_numerator": theta_err,
        "baseline_squared_error_numerator": baseline_err,
    }

    for key, value in expected.items():
        if row[key] != value:
            raise SystemExit(
                f"row {row['galaxy_id']} mismatch for {key}: expected {value}, got {row[key]}"
            )

    theta_total += theta_err
    baseline_total += baseline_err

totals = artifact["totals"]

if theta_total != totals["theta_squared_error_numerator"]:
    raise SystemExit("theta total mismatch")
if baseline_total != totals["baseline_squared_error_numerator"]:
    raise SystemExit("baseline total mismatch")
if baseline_total - theta_total != totals["improvement_numerator"]:
    raise SystemExit("improvement mismatch")
if not theta_total < baseline_total:
    raise SystemExit("fixture does not improve baseline")

for boundary in [
    "authentic SPARC empirical validation",
    "independent real-data holdout validation",
    "predictive GDM law closure",
    "low-parameter deficit-mass model closure",
    "dark matter replacement claim",
    "Lambda-CDM failure claim",
    "physical validation claim",
    "SPARC empirical victory claim",
    "PhD-complete final result claim",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
]:
    if boundary not in artifact["does_not_prove"]:
        raise SystemExit(f"missing boundary: {boundary}")

if "import Chronos.Frontier.ThetaResidualPredictionVectorExecutionGate" not in chronos_text:
    raise SystemExit("missing Chronos import")

print("THETA_RESIDUAL_PREDICTION_VECTOR_EXECUTION_GATE_OK")
