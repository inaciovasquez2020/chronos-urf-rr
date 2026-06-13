#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/derivative_identity_obligation_surface_2026_06_13.json"
doc = ROOT / "docs/status/DERIVATIVE_IDENTITY_OBLIGATION_SURFACE_2026_06_13.md"
lean = ROOT / "lean/Chronos/Frontier/DerivativeIdentityObligationSurface.lean"
root_lean = ROOT / "lean/Chronos.lean"

for path in [artifact, doc, lean, root_lean]:
    assert path.exists(), f"missing: {path}"

data = json.loads(artifact.read_text())
assert data["name"] == "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE"
assert data["status"] == "OBLIGATION_SURFACE_ONLY_DERIVATIVE_IDENTITY_NOT_ANALYTICALLY_PROVED"
assert data["previous_object"] == "RESTRICTED_CONCENTRATION_MONOTONICITY_OBLIGATION_CLOSURE"
assert data["lean_module"] == "Chronos.Frontier.DerivativeIdentityObligationSurface"
assert data["uses"] == ["RESTRICTED_CONCENTRATION_MONOTONICITY_OBLIGATION_CLOSURE"]
assert data["obligation"] == "derivativeIdentity : forall t : Real, deriv Q t = FluxDefect t"
assert data["next_admissible_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF"

for obj in [
    "DerivativeIdentityObligationData",
    "DerivativeIdentityObligation",
    "DerivativeIdentityObligationSurfaceHypotheses",
    "DerivativeIdentityObligationSurfaceClosed",
    "DerivativeIdentityObligationSurface",
]:
    assert obj in data["closed_surface_objects"]

for hyp in [
    "concentrationMonotonicityObligationClosed",
    "qDifferentiable",
    "fluxDefectDefined",
    "derivativeIdentityStated",
]:
    assert hyp in data["hypotheses"]

lean_text = lean.read_text()
for token in [
    "structure DerivativeIdentityObligationData",
    "def DerivativeIdentityObligation",
    "structure DerivativeIdentityObligationSurfaceHypotheses",
    "def DerivativeIdentityObligationSurfaceClosed",
    "theorem DerivativeIdentityObligationSurface",
    "deriv D.Q t = D.FluxDefect t",
]:
    assert token in lean_text, f"missing Lean token: {token}"

assert "Float" not in lean_text
for forbidden in ["sorry", "admit", "axiom", "opaque"]:
    assert forbidden not in lean_text

doc_text = doc.read_text()
for token in [
    "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE",
    "OBLIGATION_SURFACE_ONLY_DERIVATIVE_IDENTITY_NOT_ANALYTICALLY_PROVED",
    "RESTRICTED_CONCENTRATION_MONOTONICITY_OBLIGATION_CLOSURE",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    "no analytic derivation of derivativeIdentity from Einstein-matter PDE",
    "no Clay problem",
]:
    assert token in doc_text

assert "import Chronos.Frontier.DerivativeIdentityObligationSurface" in root_lean.read_text()

print("Derivative identity obligation surface verifier OK.")
print("Status: OBLIGATION_SURFACE_ONLY_DERIVATIVE_IDENTITY_NOT_ANALYTICALLY_PROVED")
print("Next admissible object: RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF")
