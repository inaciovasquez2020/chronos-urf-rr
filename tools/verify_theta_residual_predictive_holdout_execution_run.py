#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/ThetaResidualPredictiveHoldoutExecutionRun.lean"
ART = ROOT / "artifacts/chronos/theta_residual_predictive_holdout_execution_run_2026_05_29.json"
DOC = ROOT / "docs/status/THETA_RESIDUAL_PREDICTIVE_HOLDOUT_EXECUTION_RUN_2026_05_29.md"
CHRONOS = ROOT / "lean/Chronos.lean"

REQUIRED_LEAN_TOKENS = [
    "import Chronos.Frontier.ThetaResidualPredictiveHoldoutWithoutResidualAccess",
    "structure ThetaResidualPredictiveHoldoutExecutionRun",
    "gate : ThetaResidualPredictiveHoldoutWithoutResidualAccess",
    "rowCount_matches : rowCount = gate.rows.length",
    "thresholdPassed : Bool",
    "theorem ThetaResidualPredictiveHoldoutExecutionRun.nonempty_rows",
    "theorem ThetaResidualPredictiveHoldoutExecutionRun.rowCount_eq_length",
    "theorem ThetaResidualPredictiveHoldoutExecutionRun.no_residual_access",
    "theorem ThetaResidualPredictiveHoldoutExecutionRun.no_half_residual_identity_access",
    "theorem ThetaResidualPredictiveHoldoutExecutionRun.clean_rows",
    "\"EXECUTION_RUN_ONLY_NO_VALIDATION_CLAIM\"",
    "\"ThetaResidualPredictiveHoldoutIndependentValidationGate\"",
]

REQUIRED_DOC_TOKENS = [
    "Status: `EXECUTION_RUN_ONLY_NO_VALIDATION_CLAIM`",
    "ThetaResidualPredictiveHoldoutWithoutResidualAccess",
    "residualAccess = false",
    "halfResidualIdentityAccess = false",
    "nontrivial_predictive_signal_certified = false",
    "ThetaResidualPredictiveHoldoutExecutionRun.nonempty_rows",
    "ThetaResidualPredictiveHoldoutExecutionRun.rowCount_eq_length",
    "ThetaResidualPredictiveHoldoutExecutionRun.no_residual_access",
    "ThetaResidualPredictiveHoldoutExecutionRun.no_half_residual_identity_access",
    "ThetaResidualPredictiveHoldoutExecutionRun.clean_rows",
    "Does not prove:",
    "nontrivial theta predictive signal",
    "physical validation",
    "independent holdout validation result",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
    "ThetaResidualPredictiveHoldoutIndependentValidationGate",
]

REQUIRED_BOUNDARIES = [
    "nontrivial theta predictive signal",
    "predictive GDM law closure",
    "low-parameter deficit-mass model closure",
    "dark matter replacement claim",
    "Lambda-CDM failure claim",
    "physical validation",
    "independent holdout validation result",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
]

def require(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return path.read_text()

def main() -> None:
    lean = require(LEAN)
    doc = require(DOC)
    chronos = require(CHRONOS)

    for token in REQUIRED_LEAN_TOKENS:
        if token not in lean:
            raise SystemExit(f"missing Lean token: {token}")

    if "import Chronos.Frontier.ThetaResidualPredictiveHoldoutExecutionRun" not in chronos:
        raise SystemExit("missing import in lean/Chronos.lean")

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc:
            raise SystemExit(f"missing doc token: {token}")

    data = json.loads(require(ART))

    if data.get("status") != "EXECUTION_RUN_ONLY_NO_VALIDATION_CLAIM":
        raise SystemExit("artifact status mismatch")

    if data.get("closed_object") != "ThetaResidualPredictiveHoldoutExecutionRun":
        raise SystemExit("closed object mismatch")

    substantive_boundary = data.get("substantive_boundary", {})
    if substantive_boundary.get("nontrivial_predictive_signal_certified") is not False:
        raise SystemExit("artifact must preserve nontrivial_predictive_signal_certified=false")

    if substantive_boundary.get("validation_claim") is not False:
        raise SystemExit("artifact must preserve validation_claim=false")

    if data.get("next_admissible_object") != "ThetaResidualPredictiveHoldoutIndependentValidationGate":
        raise SystemExit("next admissible object mismatch")

    boundaries = data.get("does_not_prove", [])
    for boundary in REQUIRED_BOUNDARIES:
        if boundary not in boundaries:
            raise SystemExit(f"missing artifact boundary: {boundary}")
        if boundary not in doc:
            raise SystemExit(f"missing doc boundary: {boundary}")

    print("THETA_RESIDUAL_PREDICTIVE_HOLDOUT_EXECUTION_RUN_OK")

if __name__ == "__main__":
    main()
