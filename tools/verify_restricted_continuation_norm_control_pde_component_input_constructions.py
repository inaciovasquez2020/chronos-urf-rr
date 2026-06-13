#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_pde_component_input_constructions_2026_06_13.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_COMPONENT_INPUT_CONSTRUCTIONS_2026_06_13.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlPDEComponentInputConstructions.lean"
root_lean = ROOT / "lean/Chronos.lean"

for path in [artifact, doc, lean, root_lean]:
    assert path.exists(), f"missing: {path}"

data = json.loads(artifact.read_text())
lean_text = lean.read_text()
doc_text = doc.read_text()
root_text = root_lean.read_text()

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_COMPONENT_INPUT_CONSTRUCTIONS"
assert data["status"] == "CONDITIONAL_PDE_COMPONENT_INPUT_CONSTRUCTIONS"
assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_INPUT_PACKAGE_CONSTRUCTION"
assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlPDEComponentInputConstructions"

for token in [
    "RestrictedContinuationNormControlPDEComponentInputConstructionsHypotheses",
    "RestrictedContinuationNormControlPDEComponentInputConstructionsPackageHypotheses",
    "RestrictedContinuationNormControlPDEComponentInputConstructionsClosed",
    "theorem RestrictedContinuationNormControlPDEComponentInputConstructions",
    "theorem RestrictedContinuationNormControlAnalyticEstimateFromPDEComponentInputs",
    "bridgeComponentConstruction",
    "derivativeIdentityComponentConstruction",
    "fluxNonnegativityComponentConstruction",
    "bootstrapBoundsComponentConstruction",
]:
    assert token in lean_text, f"missing Lean token: {token}"

for forbidden in ["sorry", "admit", "axiom", "opaque"]:
    assert forbidden not in lean_text, f"forbidden token in Lean: {forbidden}"

for token in [
    "CONDITIONAL_PDE_COMPONENT_INPUT_CONSTRUCTIONS",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_INPUT_PACKAGE_CONSTRUCTION",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_COMPONENT_ANALYTIC_ESTIMATES",
]:
    assert token in doc_text, f"missing doc token: {token}"

assert "import Chronos.Frontier.RestrictedContinuationNormControlPDEComponentInputConstructions" in root_text

print("Restricted continuation norm-control PDE component input constructions verifier OK.")
print("Status: CONDITIONAL_PDE_COMPONENT_INPUT_CONSTRUCTIONS")
print("Remaining missing object: RESTRICTED_CONTINUATION_NORM_CONTROL_COMPONENT_ANALYTIC_ESTIMATES")
