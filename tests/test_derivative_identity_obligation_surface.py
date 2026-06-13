import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_artifact():
    return json.loads(
        (ROOT / "artifacts/chronos/derivative_identity_obligation_surface_2026_06_13.json").read_text()
    )


def test_derivative_identity_artifact_status():
    data = load_artifact()
    assert data["name"] == "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE"
    assert data["status"] == "OBLIGATION_SURFACE_ONLY_DERIVATIVE_IDENTITY_NOT_ANALYTICALLY_PROVED"
    assert data["previous_object"] == "RESTRICTED_CONCENTRATION_MONOTONICITY_OBLIGATION_CLOSURE"
    assert data["lean_module"] == "Chronos.Frontier.DerivativeIdentityObligationSurface"
    assert data["uses"] == ["RESTRICTED_CONCENTRATION_MONOTONICITY_OBLIGATION_CLOSURE"]
    assert data["obligation"] == "derivativeIdentity : forall t : Real, deriv Q t = FluxDefect t"
    assert data["next_admissible_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF"


def test_derivative_identity_closed_surface_objects():
    data = load_artifact()
    for obj in [
        "DerivativeIdentityObligationData",
        "DerivativeIdentityObligation",
        "DerivativeIdentityObligationSurfaceHypotheses",
        "DerivativeIdentityObligationSurfaceClosed",
        "DerivativeIdentityObligationSurface",
    ]:
        assert obj in data["closed_surface_objects"]


def test_derivative_identity_hypotheses():
    data = load_artifact()
    for hyp in [
        "concentrationMonotonicityObligationClosed",
        "qDifferentiable",
        "fluxDefectDefined",
        "derivativeIdentityStated",
    ]:
        assert hyp in data["hypotheses"]


def test_derivative_identity_boundaries_preserved():
    data = load_artifact()
    for token in [
        "obligation surface only",
        "derivativeIdentity is not analytically proved from Einstein-matter PDE",
        "does not prove the physical flux identity",
        "does not prove unrestricted gravity closure",
        "does not prove Chronos-RR",
        "does not prove H4.1/FGL",
        "does not prove P vs NP",
        "does not prove any Clay problem",
    ]:
        assert token in data["boundary"]


def test_derivative_identity_lean_surface_terms():
    text = (ROOT / "lean/Chronos/Frontier/DerivativeIdentityObligationSurface.lean").read_text()
    for token in [
        "structure DerivativeIdentityObligationData",
        "def DerivativeIdentityObligation",
        "structure DerivativeIdentityObligationSurfaceHypotheses",
        "def DerivativeIdentityObligationSurfaceClosed",
        "theorem DerivativeIdentityObligationSurface",
        "deriv D.Q t = D.FluxDefect t",
    ]:
        assert token in text


def test_derivative_identity_lean_no_fake_float_derivative_or_debt():
    text = (ROOT / "lean/Chronos/Frontier/DerivativeIdentityObligationSurface.lean").read_text()
    assert "Float" not in text
    for forbidden in ["sorry", "admit", "axiom", "opaque"]:
        assert forbidden not in text


def test_derivative_identity_doc_boundaries():
    text = (ROOT / "docs/status/DERIVATIVE_IDENTITY_OBLIGATION_SURFACE_2026_06_13.md").read_text()
    assert "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE" in text
    assert "OBLIGATION_SURFACE_ONLY_DERIVATIVE_IDENTITY_NOT_ANALYTICALLY_PROVED" in text
    assert "RESTRICTED_CONCENTRATION_MONOTONICITY_OBLIGATION_CLOSURE" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF" in text
    assert "no analytic derivation of derivativeIdentity from Einstein-matter PDE" in text
    assert "no Clay problem" in text


def test_derivative_identity_root_import():
    text = (ROOT / "lean/Chronos.lean").read_text()
    assert "import Chronos.Frontier.DerivativeIdentityObligationSurface" in text


def test_derivative_identity_verifier_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_derivative_identity_obligation_surface.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "verifier OK" in result.stdout
