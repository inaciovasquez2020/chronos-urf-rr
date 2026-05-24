from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/r2_promotion_proof_obstruction_certificate_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/R2PromotionProofObstructionCertificate.lean")

def test_r2_promotion_obstruction_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_r2_promotion_proof_obstruction_certificate.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R2_PROMOTION_PROOF_OBSTRUCTION_CERTIFICATE_OK" in result.stdout

def test_r2_counterexample_harness_target_passes():
    result = subprocess.run(
        ["python3", "tools/check_r2_promotion_counterexample_search_harness.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R2_PROMOTION_COUNTEREXAMPLE_SEARCH_HARNESS_TARGET_OK" in result.stdout

def test_r2_artifact_keeps_target_open():
    data = json.loads(ART.read_text())
    assert data["selected_target"] == "R2PromotionProofTarget"
    assert data["target_state"] == "OPEN"
    assert "R2_PROMOTION_OBSTRUCTION_ELIMINATION_PROOF" in data["next_missing_objects"]

def test_r2_lean_names_reduction_without_closing_target():
    text = LEAN.read_text()
    assert "def R2PromotionProofTargetReductionFromObstructionElimination" in text
    assert "theorem r2_promotion_proof_target_reduction_from_obstruction_elimination" in text
    assert "theorem r2_promotion_proof_target :" not in text

def test_r2_boundary_blocks_overclaims():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "R2PromotionProofTarget" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
