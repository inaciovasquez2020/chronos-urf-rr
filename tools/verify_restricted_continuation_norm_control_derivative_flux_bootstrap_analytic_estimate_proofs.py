#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_derivative_flux_bootstrap_analytic_estimate_proofs_2026_06_13.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS_2026_06_13.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofs.lean"
root_lean = ROOT / "lean/Chronos.lean"

for path in [artifact, doc, lean, root_lean]:
    assert path.exists(), f"missing: {path}"

data = json.loads(artifact.read_text())
lean_text = lean.read_text()
doc_text = doc.read_text()
root_text = root_lean.read_text()

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS"
assert data["status"] == "CONDITIONAL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS"
assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_COMPONENT_ANALYTIC_ESTIMATES"
assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofs"

for token in [
    "RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofsHypotheses",
    "RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofsComponentHypotheses",
    "RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofsClosed",
    "theorem RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofs",
    "theorem RestrictedContinuationNormControlAnalyticEstimateFromDerivativeFluxBootstrapProofs",
    "bridgeAnalyticEstimateProof",
    "derivativeIdentityAnalyticEstimateProof",
    "fluxNonnegativityAnalyticEstimateProof",
    "bootstrapBoundsAnalyticEstimateProof",
]:
    assert token in lean_text, f"missing Lean token: {token}"

for forbidden in ["sorry", "admit", "axiom", "opaque"]:
    assert forbidden not in lean_text, f"forbidden token in Lean: {forbidden}"

for token in [
    "CONDITIONAL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_COMPONENT_ANALYTIC_ESTIMATES",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD",
]:
    assert token in doc_text, f"missing doc token: {token}"

assert "import Chronos.Frontier.RestrictedContinuationNormControlDerivativeFluxBootstrapAnalyticEstimateProofs" in root_text

print("Restricted continuation norm-control derivative flux bootstrap analytic estimate proofs verifier OK.")
print("Status: CONDITIONAL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS")
print("Remaining missing object: RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD")
