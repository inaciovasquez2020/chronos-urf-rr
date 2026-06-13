import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_artifact():
    return json.loads(
        (ROOT / "artifacts/chronos/restricted_continuation_norm_control_estimate_obligation_surface_2026_06_13.json").read_text()
    )


def test_estimate_surface_artifact_status():
    data = load_artifact()
    assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_OBLIGATION_SURFACE"
    assert data["status"] == "OBLIGATION_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED"
    assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE"
    assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlEstimateObligationSurface"
    assert data["next_admissible_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_PROOF_BRIDGE"


def test_estimate_surface_uses():
    data = load_artifact()
    assert data["uses"] == [
        "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE",
        "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE",
        "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    ]


def test_estimate_surface_closed_surface_objects():
    data = load_artifact()
    for obj in [
        "RestrictedContinuationNormControlEstimateData",
        "RestrictedContinuationNormControlEstimateObligation",
        "RestrictedContinuationNormControlEstimateObligationSurfaceHypotheses",
        "RestrictedContinuationNormControlEstimateObligationSurfaceClosed",
        "RestrictedContinuationNormControlEstimateObligationSurface",
    ]:
        assert obj in data["closed_surface_objects"]


def test_estimate_surface_hypotheses():
    data = load_artifact()
    for hyp in [
        "derivativeIdentityBridgeAvailable",
        "continuationProofSurfaceAvailable",
        "estimateObligationStated",
    ]:
        assert hyp in data["hypotheses"]


def test_estimate_surface_boundaries_preserved():
    data = load_artifact()
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
        assert token in data["boundary"]


def test_estimate_surface_lean_surface_terms():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlEstimateObligationSurface.lean").read_text()
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
        assert token in text


def test_estimate_surface_lean_no_fake_float_derivative_or_debt():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlEstimateObligationSurface.lean").read_text()
    assert "Float" not in text
    for forbidden in ["sorry", "admit", "axiom", "opaque"]:
        assert forbidden not in text


def test_estimate_surface_doc_boundaries():
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_OBLIGATION_SURFACE_2026_06_13.md").read_text()
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_OBLIGATION_SURFACE" in text
    assert "OBLIGATION_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_PROOF_BRIDGE" in text
    assert "does not prove any Clay problem" in text


def test_estimate_surface_root_import():
    text = (ROOT / "lean/Chronos.lean").read_text()
    assert "import Chronos.Frontier.RestrictedContinuationNormControlEstimateObligationSurface" in text


def test_estimate_surface_verifier_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_restricted_continuation_norm_control_estimate_obligation_surface.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "verifier OK" in result.stdout
