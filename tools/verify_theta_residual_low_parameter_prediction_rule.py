#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/ThetaResidualLowParameterPredictionRule.lean"
ART = ROOT / "artifacts/sparc/theta_residual_low_parameter_prediction_rule_2026_05_29.json"
DOC = ROOT / "docs/status/THETA_RESIDUAL_LOW_PARAMETER_PREDICTION_RULE_2026_05_29.md"
CHRONOS = ROOT / "lean/Chronos.lean"

for path in [LEAN, ART, DOC, CHRONOS]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = LEAN.read_text()
doc_text = DOC.read_text()
chronos_text = CHRONOS.read_text()
artifact = json.loads(ART.read_text())

required_lean_tokens = [
    "ThetaResidualLowParameterPredictionRule",
    "ThetaResidualLowParameterInput",
    "thetaResidual",
    "thetaDeficitNumerator",
    "thetaPredictionNumerator",
    "thetaRuleV1",
    "thetaRuleV1_projects_to_concrete_model",
    "thetaRuleV1_theta_denominator_positive",
    "thetaRuleV1_theta_strictly_below_one",
    "thetaRuleV1_has_frozen_before_likelihood_guard",
    "thetaRuleV1_has_low_parameter_guard",
    "thetaRuleV1_has_no_empirical_validation_claim",
    "thetaRuleV1_has_no_physical_replacement_claim",
    "thetaResidual_zero_when_observed_le_baryonic",
    "thetaPredictionNumerator_at_zero_residual",
]

required_doc_tokens = [
    "LOW_PARAMETER_RULE_SURFACE_ONLY_NO_EMPIRICAL_VALIDATION",
    "Does not prove: authentic SPARC empirical validation.",
    "Does not prove: independent real-data holdout validation.",
    "Does not prove: predictive GDM law closure.",
    "Does not prove: low-parameter deficit-mass model closure.",
    "Does not prove: dark matter replacement claim.",
    "Does not prove: Lambda-CDM failure claim.",
    "Does not prove: physical validation claim.",
    "Does not prove: SPARC empirical victory claim.",
    "Does not prove: PhD-complete final result claim.",
    "Does not prove: unrestricted Chronos-RR.",
    "Does not prove: unrestricted H4.1/FGL.",
    "Does not prove: P vs NP.",
    "Does not prove: Clay problem.",
    "ThetaResidualPredictionVectorExecutionGate",
]

required_artifact = {
    "id": "THETA_RESIDUAL_LOW_PARAMETER_PREDICTION_RULE_2026_05_29",
    "status": "LOW_PARAMETER_RULE_SURFACE_ONLY_NO_EMPIRICAL_VALIDATION",
    "object_name": "ThetaResidualLowParameterPredictionRule",
    "extends": "ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel",
    "next_missing_object": "ThetaResidualPredictionVectorExecutionGate",
}

for token in required_lean_tokens:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in required_doc_tokens:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

for key, expected in required_artifact.items():
    actual = artifact.get(key)
    if actual != expected:
        raise SystemExit(f"artifact mismatch for {key}: expected {expected!r}, got {actual!r}")

theta = artifact.get("theta_representation", {})
if theta.get("theta_numerator") != 1:
    raise SystemExit("unexpected theta numerator")
if theta.get("theta_denominator") != 2:
    raise SystemExit("unexpected theta denominator")
if "numerator < denominator" not in theta.get("domain", ""):
    raise SystemExit("missing theta domain boundary")

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
    if boundary not in artifact.get("does_not_prove", []):
        raise SystemExit(f"missing artifact boundary: {boundary}")

import_line = "import Chronos.Frontier.ThetaResidualLowParameterPredictionRule"
if import_line not in chronos_text:
    raise SystemExit(f"missing Chronos import: {import_line}")

dependency_import = "import Chronos.Frontier.ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel"
if dependency_import not in lean_text:
    raise SystemExit("missing dependency import in theta rule Lean module")

print("THETA_RESIDUAL_LOW_PARAMETER_PREDICTION_RULE_OK")
