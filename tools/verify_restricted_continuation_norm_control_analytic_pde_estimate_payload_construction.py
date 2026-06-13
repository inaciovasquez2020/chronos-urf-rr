#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_analytic_pde_estimate_payload_construction_2026_06_13.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION_2026_06_13.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstruction.lean"
root_lean = ROOT / "lean/Chronos.lean"

for path in [artifact, doc, lean, root_lean]:
    assert path.exists(), f"missing: {path}"

data = json.loads(artifact.read_text())
lean_text = lean.read_text()
doc_text = doc.read_text()
root_text = root_lean.read_text()

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION"
assert data["status"] == "CONDITIONAL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION"
assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD"
assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstruction"

for token in [
    "RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionHypotheses",
    "RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionPayload",
    "RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstructionClosed",
    "theorem RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstruction",
    "theorem RestrictedContinuationNormControlAnalyticEstimateFromConstructedAnalyticPDEEstimatePayload",
    "bridgePayloadConstruction",
    "derivativeIdentityPayloadConstruction",
    "fluxNonnegativityPayloadConstruction",
    "bootstrapBoundsPayloadConstruction",
]:
    assert token in lean_text, f"missing Lean token: {token}"

for forbidden in ["sorry", "admit", "axiom", "opaque"]:
    assert forbidden not in lean_text, f"forbidden token in Lean: {forbidden}"

for token in [
    "CONDITIONAL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_ANALYTIC_PROOFS",
]:
    assert token in doc_text, f"missing doc token: {token}"

assert "import Chronos.Frontier.RestrictedContinuationNormControlAnalyticPDEEstimatePayloadConstruction" in root_text

print("Restricted continuation norm-control analytic PDE estimate payload construction verifier OK.")
print("Status: CONDITIONAL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION")
print("Remaining missing object: RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_ANALYTIC_PROOFS")
