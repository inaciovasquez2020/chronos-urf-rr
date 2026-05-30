#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ART = Path("artifacts/chronos/ytr_gravity_tidal_derivative_real_dataset_falsification_run_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/YtRGravityTidalDerivativeRealDatasetFalsificationRun.lean")
DOC = Path("docs/status/YTR_GRAVITY_TIDAL_DERIVATIVE_REAL_DATASET_FALSIFICATION_RUN_2026_05_29.md")

REQUIRED_ARTIFACT_TOKENS = [
    "YTR_GRAVITY_TIDAL_DERIVATIVE_REAL_DATASET_FALSIFICATION_RUN_2026_05_29",
    "REAL_DATA_FALSIFICATION_GATE_ONLY",
    "tidalDerivativeCoefficient",
    "radial_gravity_gradient_dg_dr",
    "GRACEFO_L2_JPL_MONTHLY_0063",
    "standard_GR_or_Newtonian_geodesy_prediction",
    "measurement_uncertainty_plus_model_error_bound",
    "candidate_error_greater_or_equal_baseline_error_or_no_nontrivial_residual_survives_uncertainty",
]

REQUIRED_LEAN_TOKENS = [
    "TidalDerivativeCoefficientRename",
    "EarthScaleTidalDerivativeConstants",
    "AuthenticPublicGravityDatasetPayloadBinding",
    "GRBaselineComparisonMetricWithTolerance",
    "ExplicitFalsificationCertificate",
    "YtRGravityTidalDerivativeRealDatasetFalsificationRun",
    "tidalDerivativeCoefficientRename_closed",
    "ytrGravityTidalDerivativeRealDatasetFalsificationRun_boundary_closed",
]

FORBIDDEN_OVERCLAIMS = [
    "GR failure proved",
    "new gravity proved",
    "dark matter replaced",
    "Lambda-CDM failure proved",
    "quantum gravity proved",
    "Clay problem solved",
]

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(LEAN.exists(), f"missing Lean file: {LEAN}")
    require(DOC.exists(), f"missing status doc: {DOC}")

    data = json.loads(ART.read_text())
    art_text = ART.read_text()
    lean_text = LEAN.read_text()
    doc_text = DOC.read_text()

    require(data["status"] == "REAL_DATA_FALSIFICATION_GATE_ONLY", "bad status")
    require(data["changes"]["rename"]["from"] == "K_g", "old symbol not recorded")
    require(data["changes"]["rename"]["to"] == "tidalDerivativeCoefficient", "new symbol not recorded")
    require(data["changes"]["public_dataset_payload_binding"]["dataset"] == "GRACEFO_L2_JPL_MONTHLY_0063", "dataset not bound")
    require(data["changes"]["falsification_certificate"]["disconfirmation_path_exists"] is True, "no disconfirmation path")

    for token in REQUIRED_ARTIFACT_TOKENS:
        require(token in art_text, f"artifact missing token: {token}")

    for token in REQUIRED_LEAN_TOKENS:
        require(token in lean_text, f"Lean missing token: {token}")

    for token in FORBIDDEN_OVERCLAIMS:
        require(token not in art_text, f"artifact overclaim: {token}")
        require(token not in lean_text, f"Lean overclaim: {token}")
        require(token not in doc_text, f"doc overclaim: {token}")

    print("YTR_GRAVITY_TIDAL_DERIVATIVE_REAL_DATASET_FALSIFICATION_RUN_OK")

if __name__ == "__main__":
    main()
