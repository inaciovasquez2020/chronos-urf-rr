import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_artifact():
    return json.loads(
        (ROOT / "artifacts/chronos/restricted_continuation_norm_control_derivative_identity_bridge_2026_06_13.json").read_text()
    )


def test_bridge_artifact_status():
    data = load_artifact()
    assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE"
    assert data["status"] == "BRIDGE_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED"
    assert data["previous_object"] == "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE"
    assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlDerivativeIdentityBridge"
    assert data["next_admissible_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_ESTIMATE_OBLIGATION_SURFACE"


def test_bridge_uses():
    data = load_artifact()
    assert data["uses"] == [
        "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE",
        "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    ]


def test_bridge_closed_surface_objects():
    data = load_artifact()
    for obj in [
        "RestrictedContinuationNormControlDerivativeIdentityBridgeData",
        "RestrictedContinuationNormControlDerivativeIdentityBridgeObligation",
        "RestrictedContinuationNormControlDerivativeIdentityBridgeHypotheses",
        "RestrictedContinuationNormControlDerivativeIdentityBridgeClosed",
        "RestrictedContinuationNormControlDerivativeIdentityBridge",
    ]:
        assert obj in data["closed_surface_objects"]


def test_bridge_hypotheses():
    data = load_artifact()
    for hyp in [
        "derivativeIdentityObligationSurfaceAvailable",
        "restrictedContinuationNormControlProofSurfaceAvailable",
        "bridgeObligationStated",
    ]:
        assert hyp in data["hypotheses"]


def test_bridge_boundaries_preserved():
    data = load_artifact()
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
        assert token in data["boundary"]


def test_bridge_lean_surface_terms():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlDerivativeIdentityBridge.lean").read_text()
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
        assert token in text


def test_bridge_lean_no_fake_float_derivative_or_debt():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlDerivativeIdentityBridge.lean").read_text()
    assert "Float" not in text
    for forbidden in ["sorry", "admit", "axiom", "opaque"]:
        assert forbidden not in text


def test_bridge_doc_boundaries():
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE_2026_06_13.md").read_text()
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_IDENTITY_BRIDGE" in text
    assert "BRIDGE_SURFACE_ONLY_CONTINUATION_ESTIMATE_NOT_ANALYTICALLY_PROVED" in text
    assert "DERIVATIVE_IDENTITY_OBLIGATION_SURFACE" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF" in text
    assert "does not prove any Clay problem" in text


def test_bridge_root_import():
    text = (ROOT / "lean/Chronos.lean").read_text()
    assert "import Chronos.Frontier.RestrictedContinuationNormControlDerivativeIdentityBridge" in text


def test_bridge_verifier_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_restricted_continuation_norm_control_derivative_identity_bridge.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "verifier OK" in result.stdout
