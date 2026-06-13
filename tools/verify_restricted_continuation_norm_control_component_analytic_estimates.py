#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_component_analytic_estimates_2026_06_13.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_COMPONENT_ANALYTIC_ESTIMATES_2026_06_13.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlComponentAnalyticEstimates.lean"
root_lean = ROOT / "lean/Chronos.lean"

for path in [artifact, doc, lean, root_lean]:
    assert path.exists(), f"missing: {path}"

data = json.loads(artifact.read_text())
lean_text = lean.read_text()
doc_text = doc.read_text()
root_text = root_lean.read_text()

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_COMPONENT_ANALYTIC_ESTIMATES"
assert data["status"] == "CONDITIONAL_COMPONENT_ANALYTIC_ESTIMATES"
assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_COMPONENT_INPUT_CONSTRUCTIONS"
assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlComponentAnalyticEstimates"

for token in [
    "RestrictedContinuationNormControlComponentAnalyticEstimatesHypotheses",
    "RestrictedContinuationNormControlComponentAnalyticEstimatesComponentInputHypotheses",
    "RestrictedContinuationNormControlComponentAnalyticEstimatesClosed",
    "theorem RestrictedContinuationNormControlComponentAnalyticEstimates",
    "theorem RestrictedContinuationNormControlAnalyticEstimateFromComponentAnalyticEstimates",
    "bridgeAnalyticEstimate",
    "derivativeIdentityAnalyticEstimate",
    "fluxNonnegativityAnalyticEstimate",
    "bootstrapBoundsAnalyticEstimate",
]:
    assert token in lean_text, f"missing Lean token: {token}"

for forbidden in ["sorry", "admit", "axiom", "opaque"]:
    assert forbidden not in lean_text, f"forbidden token in Lean: {forbidden}"

for token in [
    "CONDITIONAL_COMPONENT_ANALYTIC_ESTIMATES",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_COMPONENT_INPUT_CONSTRUCTIONS",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS",
]:
    assert token in doc_text, f"missing doc token: {token}"

assert "import Chronos.Frontier.RestrictedContinuationNormControlComponentAnalyticEstimates" in root_text

print("Restricted continuation norm-control component analytic estimates verifier OK.")
print("Status: CONDITIONAL_COMPONENT_ANALYTIC_ESTIMATES")
print("Remaining missing object: RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS")
