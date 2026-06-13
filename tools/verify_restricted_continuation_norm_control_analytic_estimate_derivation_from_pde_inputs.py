#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_analytic_estimate_derivation_from_pde_inputs_2026_06_13.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_DERIVATION_FROM_PDE_INPUTS_2026_06_13.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputs.lean"
root_lean = ROOT / "lean/Chronos.lean"

for path in [artifact, doc, lean, root_lean]:
    assert path.exists(), f"missing: {path}"

data = json.loads(artifact.read_text())
lean_text = lean.read_text()
doc_text = doc.read_text()
root_text = root_lean.read_text()

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_DERIVATION_FROM_PDE_INPUTS"
assert data["status"] == "CONDITIONAL_DERIVATION_FROM_PDE_INPUT_PACKAGE"
assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_PROOF"
assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputs"

for token in [
    "RestrictedContinuationNormControlPDEInputPackage",
    "RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputsClosed",
    "theorem RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputs",
    "RestrictedContinuationNormControlAnalyticEstimateProof",
    "bridgeAvailable",
    "derivativeIdentityDerivedFromPDE",
    "fluxNonnegativityDerivedFromPDE",
    "bootstrapBoundsDerivedFromPDE",
]:
    assert token in lean_text, f"missing Lean token: {token}"

for forbidden in ["sorry", "admit", "axiom", "opaque"]:
    assert forbidden not in lean_text, f"forbidden token in Lean: {forbidden}"

for token in [
    "CONDITIONAL_DERIVATION_FROM_PDE_INPUT_PACKAGE",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_PROOF",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_INPUT_PACKAGE_CONSTRUCTION",
]:
    assert token in doc_text, f"missing doc token: {token}"

assert "import Chronos.Frontier.RestrictedContinuationNormControlAnalyticEstimateDerivationFromPDEInputs" in root_text

print("Restricted continuation norm-control analytic estimate derivation from PDE inputs verifier OK.")
print("Status: CONDITIONAL_DERIVATION_FROM_PDE_INPUT_PACKAGE")
print("Remaining missing object: RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_INPUT_PACKAGE_CONSTRUCTION")
