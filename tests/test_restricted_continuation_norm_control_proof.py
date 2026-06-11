import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_proof_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/restricted_continuation_norm_control_proof_2026_06_11.json").read_text()
    )
    assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF"
    assert data["status"] == "PROOF_OBLIGATION_SURFACE_ONLY_NO_CONTINUATION_NORM_CONTROL_PROOF"
    assert data["previous_object"] == "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF"
    assert data["next_admissible_object"] == "PACKAGE_COMPATIBILITY_PROOF"
    assert "no unconditional restricted continuation norm control theorem" in data["boundary"]
    assert "no concrete analytic Einstein-matter estimate package proof" in data["boundary"]

def test_restricted_continuation_norm_control_proof_doc():
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF_2026_06_11.md").read_text()
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF" in text
    assert "PACKAGE_COMPATIBILITY_PROOF" in text
    assert "unconditional restricted continuation norm control theorem" in text

def test_restricted_continuation_norm_control_proof_lean_surface():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlProof.lean").read_text()
    assert "structure RestrictedContinuationNormControlProofSurfaceData" in text
    assert "structure RestrictedContinuationNormControlProofSurfaceObligations" in text
    assert "theorem RestrictedContinuationNormControlProofSurface" in text
    assert "PROOF_OBLIGATION_SURFACE_ONLY_NO_CONTINUATION_NORM_CONTROL_PROOF" in text
