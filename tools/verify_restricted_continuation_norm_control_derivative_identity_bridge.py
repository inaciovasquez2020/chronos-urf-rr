#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_derivative_identity_bridge_2026_06_13.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE_2026_06_13.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlDerivativeIdentityBridge.lean"
root_lean = ROOT / "lean/Chronos.lean"

for path in [artifact, doc, lean, root_lean]:
    assert path.exists(), f"missing: {path}"

data = json.loads(artifact.read_text())

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE"
assert data["status"] == "BRIDGE_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED"
assert data["previous_object"] == "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE"
assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlDerivativeIdentityBridge"
assert data["uses"] == [
    "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
]
assert data["next_admissible_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_OBLIGATION_SURFACE"

for obj in [
    "RestrictedContinuationNormControlDerivativeIdentityBridgeData",
    "RestrictedContinuationNormControlDerivativeIdentityBridgeObligation",
    "RestrictedContinuationNormControlDerivativeIdentityBridgeHypotheses",
    "RestrictedContinuationNormControlDerivativeIdentityBridgeClosed",
    "RestrictedContinuationNormControlDerivativeIdentityBridge",
]:
    assert obj in data["closed_surface_objects"], f"missing object: {obj}"

for hyp in [
    "derivativeIdentityObligationSurfaceAvailable",
    "restrictedContinuationNormControlProofSurfaceAvailable",
    "bridgeObligationStated",
]:
    assert hyp in data["hypotheses"], f"missing hypothesis: {hyp}"

for token in [
    "bridge surface only",
    "continuation estimate is not analytically proved",
    "does not prove restricted continuation norm-control estimate from PDE",
    "does not prove unrestricted gravity closure",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]:
    assert token in data["boundary"], f"missing boundary: {token}"

lean_text = lean.read_text()
for token in [
    "import Chronos.Frontier.DerivativeIdentityObligationSurface",
    "import Chronos.Frontier.RestrictedContinuationNormControlProof",
    "structure RestrictedContinuationNormControlDerivativeIdentityBridgeData",
    "def RestrictedContinuationNormControlDerivativeIdentityBridgeObligation",
    "structure RestrictedContinuationNormControlDerivativeIdentityBridgeHypotheses",
    "def RestrictedContinuationNormControlDerivativeIdentityBridgeClosed",
    "theorem RestrictedContinuationNormControlDerivativeIdentityBridge",
    "DerivativeIdentityObligation D.derivativeIdentityData",
]:
    assert token in lean_text, f"missing Lean token: {token}"

assert "Float" not in lean_text
for forbidden in ["sorry", "admit", "axiom", "opaque"]:
    assert forbidden not in lean_text, f"forbidden token in Lean: {forbidden}"

doc_text = doc.read_text()
for token in [
    "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE",
    "BRIDGE_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED",
    "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    "does not prove any Clay problem",
]:
    assert token in doc_text, f"missing doc token: {token}"

assert "import Chronos.Frontier.RestrictedContinuationNormControlDerivativeIdentityBridge" in root_lean.read_text()

print("Restricted continuation norm-control derivative identity bridge verifier OK.")
print("Status: BRIDGE_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED")
print("Next admissible object: RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_OBLIGATION_SURFACE")
