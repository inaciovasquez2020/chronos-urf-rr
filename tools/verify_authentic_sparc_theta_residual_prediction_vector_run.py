#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_OUT = ROOT / "artifacts/sparc/authentic_sparc_theta_residual_prediction_vector_run_2026_05_29.csv"
ART = ROOT / "artifacts/sparc/authentic_sparc_theta_residual_prediction_vector_run_2026_05_29.json"
BASELINE = ROOT / "artifacts/sparc/rotation_curve_step3_5_2026_05_28/BASELINE_MODEL_PREDICTION_VECTOR_2026_05_28.csv"
DOC = ROOT / "docs/status/AUTHENTIC_SPARC_THETA_RESIDUAL_PREDICTION_VECTOR_RUN_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/AuthenticSPARCThetaResidualPredictionVectorRun.lean"

STATUS = "REPOSITORY_ARCHIVED_SPARC_DERIVED_NUMERIC_RUN_NO_RAW_PAYLOAD_CLAIM"

for path in [CSV_OUT, ART, BASELINE, DOC, LEAN]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")

with ART.open() as f:
    artifact = json.load(f)

with CSV_OUT.open(newline="") as f:
    rows = list(csv.DictReader(f))

with BASELINE.open(newline="") as f:
    baseline_rows = list(csv.DictReader(f))

if not rows:
    raise SystemExit("theta residual output CSV has no rows")

if len(rows) != len(baseline_rows):
    raise SystemExit(f"row count mismatch: output={len(rows)} baseline={len(baseline_rows)}")

galaxies = {row["galaxy_id"] for row in rows if row.get("galaxy_id")}
if not galaxies:
    raise SystemExit("no galaxy_id values found")

row_count = int(artifact.get("row_count", -1))
galaxy_count = int(artifact.get("galaxy_count", -1))
theta_squared_error = float(artifact.get("theta_squared_error", -1.0))
baseline_squared_error = float(artifact.get("baseline_squared_error", -1.0))
improvement = float(artifact.get("improvement", 0.0))
theta_improves_baseline = bool(artifact.get("theta_improves_baseline", False))

if artifact.get("status") != STATUS:
    raise SystemExit(f"bad status: {artifact.get('status')}")

if row_count != len(rows):
    raise SystemExit(f"artifact row_count mismatch: {row_count} != {len(rows)}")

if galaxy_count != len(galaxies):
    raise SystemExit(f"artifact galaxy_count mismatch: {galaxy_count} != {len(galaxies)}")

if theta_squared_error < 0.0:
    raise SystemExit("theta_squared_error is negative")

if baseline_squared_error < 0.0:
    raise SystemExit("baseline_squared_error is negative")

expected_improvement = baseline_squared_error - theta_squared_error
if abs(expected_improvement - improvement) > max(1e-6, abs(expected_improvement) * 1e-9):
    raise SystemExit("improvement does not equal baseline_squared_error - theta_squared_error")

if theta_improves_baseline != (theta_squared_error < baseline_squared_error):
    raise SystemExit("theta_improves_baseline flag disagrees with squared-error comparison")

if not theta_improves_baseline:
    raise SystemExit("theta_improves_baseline is false")

for row in rows:
    baseline_term = float(row["baseline_squared_error_term"])
    theta_term = float(row["theta_squared_error_term"])
    if baseline_term < 0.0:
        raise SystemExit("negative baseline squared-error term")
    if theta_term < 0.0:
        raise SystemExit("negative theta squared-error term")

doc_text = DOC.read_text()
for token in [
    "repository-archived SPARC-derived numeric run only",
    "no raw SPARC payload authenticity newly verified",
    "no authentic SPARC empirical validation",
    "no independent real-data holdout validation",
    "no predictive GDM law closure",
    "no low-parameter deficit-mass model closure",
    "no dark matter replacement claim",
    "no Lambda-CDM failure claim",
    "no physical validation claim",
    "no SPARC empirical victory claim",
    "no PhD-complete final result claim",
    "no unrestricted Chronos-RR",
    "no unrestricted H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]:
    if token not in doc_text:
        raise SystemExit(f"missing boundary token: {token}")

lean_text = LEAN.read_text()
for token in [
    "AuthenticSPARCThetaResidualPredictionVectorRun",
    "theta",
    "residual",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

print("AUTHENTIC_SPARC_THETA_RESIDUAL_PREDICTION_VECTOR_RUN_OK")
