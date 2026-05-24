from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/r3_promotion_proof_obstruction_certificate_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/R3PromotionProofObstructionCertificate.lean")

def test_r3_promotion_obstruction_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_r3_promotion_proof_obstruction_certificate.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R3_PROMOTION_PROOF_OBSTRUCTION_CERTIFICATE_OK" in result.stdout

def test_r3_counterexample_harness_target_passes():
    result = subprocess.run(
        ["python3", "tools/check_r3_promotion_counterexample_search_harness.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R3_PROMOTION_COUNTEREXAMPLE_SEARCH_HARNESS_TARGET_OK" in result.stdout

def test_r3_artifact_keeps_target_open():
    data = json.loads(ART.read_text())
    assert data["selected_target"] == "R3PromotionProofTarget"
    assert data["target_state"] == "OPEN"
    assert "R3_PROMOTION_OBSTRUCTION_ELIMINATION_PROOF" in data["next_missing_objects"]

def test_r3_lean_names_reduction_without_closing_target():
    text = LEAN.read_text()
    assert "def R3PromotionProofTargetReductionFromObstructionElimination" in text
    assert "theorem r3_promotion_proof_target_reduction_from_obstruction_elimination" in text
    assert "theorem r3_promotion_proof_target :" not in text

def test_r3_boundary_blocks_overclaims():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "R3PromotionProofTarget" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
