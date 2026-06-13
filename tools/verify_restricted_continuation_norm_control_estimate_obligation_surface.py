#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_estimate_obligation_surface_2026_06_13.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_OBLIGATION_SURFACE_2026_06_13.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlEstimateObligationSurface.lean"
root_lean = ROOT / "lean/Chronos.lean"

for path in [artifact, doc, lean, root_lean]:
    assert path.exists(), f"missing: {path}"

data = json.loads(artifact.read_text())

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_OBLIGATION_SURFACE"
assert data["status"] == "OBLIGATION_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED"
assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE"
assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlEstimateObligationSurface"
assert data["uses"] == [
    "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
]
assert data["next_admissible_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_PROOF_BRIDGE"

for obj in [
    "RestrictedContinuationNormControlEstimateData",
    "RestrictedContinuationNormControlEstimateObligation",
    "RestrictedContinuationNormControlEstimateObligationSurfaceHypotheses",
    "RestrictedContinuationNormControlEstimateObligationSurfaceClosed",
    "RestrictedContinuationNormControlEstimateObligationSurface",
]:
    assert obj in data["closed_surface_objects"], f"missing object: {obj}"

for hyp in [
    "derivativeIdentityBridgeAvailable",
    "continuationProofSurfaceAvailable",
    "estimateObligationStated",
]:
    assert hyp in data["hypotheses"], f"missing hypothesis: {hyp}"

for token in [
    "obligation surface only",
    "continuation estimate is not analytically proved",
    "does not prove restricted continuation norm-control estimate from PDE",
    "does not prove derivativeIdentity",
    "does not prove flux nonnegativity",
    "does not prove bootstrap bounds",
    "does not prove unrestricted gravity closure",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]:
    assert token in data["boundary"], f"missing boundary: {token}"

lean_text = lean.read_text()
for token in [
    "import Chronos.Frontier.RestrictedContinuationNormControlDerivativeIdentityBridge",
    "structure RestrictedContinuationNormControlEstimateData",
    "def RestrictedContinuationNormControlEstimateObligation",
    "structure RestrictedContinuationNormControlEstimateObligationSurfaceHypotheses",
    "def RestrictedContinuationNormControlEstimateObligationSurfaceClosed",
    "theorem RestrictedContinuationNormControlEstimateObligationSurface",
    "DerivativeIdentityObligation D.derivativeIdentityData",
    "D.fluxNonnegativityAvailable",
    "D.bootstrapBoundsAvailable",
    "D.continuationNormControlTarget",
]:
    assert token in lean_text, f"missing Lean token: {token}"

assert "Float" not in lean_text
for forbidden in ["sorry", "admit", "axiom", "opaque"]:
    assert forbidden not in lean_text, f"forbidden token in Lean: {forbidden}"

doc_text = doc.read_text()
for token in [
    "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_OBLIGATION_SURFACE",
    "OBLIGATION_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_PROOF_BRIDGE",
    "does not prove any Clay problem",
]:
    assert token in doc_text, f"missing doc token: {token}"

assert "import Chronos.Frontier.RestrictedContinuationNormControlEstimateObligationSurface" in root_lean.read_text()

print("Restricted continuation norm-control estimate obligation surface verifier OK.")
print("Status: OBLIGATION_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED")
print("Next admissible object: RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_PROOF_BRIDGE")
