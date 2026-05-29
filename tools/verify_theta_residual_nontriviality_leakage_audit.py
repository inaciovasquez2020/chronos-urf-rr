#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART = ROOT / "artifacts/sparc/theta_residual_nontriviality_leakage_audit_2026_05_29.json"
DOC = ROOT / "docs/status/THETA_RESIDUAL_NONTRIVIALITY_LEAKAGE_AUDIT_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/ThetaResidualNontrivialityLeakageAudit.lean"

STATUS = "THETA_RESIDUAL_NONTRIVIALITY_LEAKAGE_AUDIT_EXECUTED"

for path in [ART, DOC, LEAN]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")

artifact = json.loads(ART.read_text())

if artifact.get("status") != STATUS:
    raise SystemExit(f"bad status: {artifact.get('status')}")

if artifact.get("algebraic_leakage_detected") is not True:
    raise SystemExit("algebraic leakage was not detected")

if artifact.get("nontrivial_predictive_signal_certified") is not False:
    raise SystemExit("nontrivial predictive signal must not be certified")

if artifact.get("audit_conclusion") != "DETERMINISTIC_HALF_RESIDUAL_IDENTITY_EXPLAINS_75_PERCENT_SQUARED_ERROR_REDUCTION":
    raise SystemExit("unexpected audit conclusion")

for key in [
    "exact_half_error_identity_fraction",
    "exact_quarter_squared_error_fraction",
]:
    value = float(artifact[key])
    if abs(value - 1.0) > 1e-12:
        raise SystemExit(f"{key} is not exactly saturated: {value}")

ratio = float(artifact["theta_error_ratio"])
reduction = float(artifact["theta_error_reduction_fraction"])

if abs(ratio - 0.25) > 1e-12:
    raise SystemExit(f"theta_error_ratio mismatch: {ratio}")
if abs(reduction - 0.75) > 1e-12:
    raise SystemExit(f"theta_error_reduction_fraction mismatch: {reduction}")

doc_text = DOC.read_text()
for token in [
    "nontriviality leakage audit only",
    "detects algebraic reuse of residual target",
    "does not certify nontrivial predictive signal",
    "does not certify physical robustness",
    "does not certify out-of-sample physical validation",
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
    "ThetaResidualNontrivialityLeakageAudit",
    "algebraicLeakageDetected",
    "nontrivialPredictiveSignalCertified",
    "theta",
    "residual",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

print("THETA_RESIDUAL_NONTRIVIALITY_LEAKAGE_AUDIT_OK")
