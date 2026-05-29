#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART = ROOT / "artifacts/sparc/theta_residual_cross_validation_stability_run_2026_05_29.json"
CSV_OUT = ROOT / "artifacts/sparc/theta_residual_cross_validation_stability_run_2026_05_29.csv"
SOURCE = ROOT / "artifacts/sparc/authentic_sparc_theta_residual_prediction_vector_run_2026_05_29.csv"
DOC = ROOT / "docs/status/THETA_RESIDUAL_CROSS_VALIDATION_STABILITY_RUN_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/ThetaResidualCrossValidationStabilityRun.lean"

STATUS = "THETA_RESIDUAL_CROSS_VALIDATION_STABILITY_RUN_EXECUTED"
THRESHOLD = 0.65

for path in [ART, CSV_OUT, SOURCE, DOC, LEAN]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")

artifact = json.loads(ART.read_text())

with CSV_OUT.open(newline="") as f:
    fold_rows = list(csv.DictReader(f))

with SOURCE.open(newline="") as f:
    source_rows = list(csv.DictReader(f))

if artifact.get("status") != STATUS:
    raise SystemExit(f"bad status: {artifact.get('status')}")

row_count = int(artifact["row_count"])
galaxy_count = int(artifact["galaxy_count"])
fold_count = int(artifact["fold_count"])
aggregate_reduction = float(artifact["aggregate_reduction_fraction"])
mean_reduction = float(artifact["mean_fold_reduction_fraction"])
median_reduction = float(artifact["median_fold_reduction_fraction"])
min_reduction = float(artifact["min_fold_reduction_fraction"])
threshold = float(artifact["threshold_reduction_fraction"])

if row_count != len(source_rows):
    raise SystemExit("source row count mismatch")
if galaxy_count != len({row["galaxy_id"] for row in source_rows}):
    raise SystemExit("galaxy count mismatch")
if fold_count != len(fold_rows):
    raise SystemExit("fold count mismatch")
if fold_count != galaxy_count:
    raise SystemExit("fold_count must equal galaxy_count")
if abs(threshold - THRESHOLD) > 1e-12:
    raise SystemExit("threshold mismatch")

for name, value in [
    ("aggregate_reduction_fraction", aggregate_reduction),
    ("mean_fold_reduction_fraction", mean_reduction),
    ("median_fold_reduction_fraction", median_reduction),
    ("min_fold_reduction_fraction", min_reduction),
]:
    if not (-10.0 <= value <= 1.0):
        raise SystemExit(f"{name} out of bounded range: {value}")

if aggregate_reduction < THRESHOLD:
    raise SystemExit("aggregate reduction below threshold")
if mean_reduction < THRESHOLD:
    raise SystemExit("mean fold reduction below threshold")

if artifact.get("aggregate_passes_threshold") is not True:
    raise SystemExit("aggregate_passes_threshold is not true")
if artifact.get("mean_fold_passes_threshold") is not True:
    raise SystemExit("mean_fold_passes_threshold is not true")

doc_text = DOC.read_text()
for token in [
    "repository-archived theta residual cross-validation stability run only",
    "leave-one-galaxy-out accounting over archived theta output only",
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
    "ThetaResidualCrossValidationStabilityRun",
    "crossValidation",
    "theta",
    "residual",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

print("THETA_RESIDUAL_CROSS_VALIDATION_STABILITY_RUN_OK")
