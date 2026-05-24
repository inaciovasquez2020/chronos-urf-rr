from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/r1_r2_r3_promotion_obstruction_frontier_lock_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/R1R2R3PromotionObstructionFrontierLock.lean")

def test_promotion_obstruction_frontier_lock_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_r1_r2_r3_promotion_obstruction_frontier_lock.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R1_R2_R3_PROMOTION_OBSTRUCTION_FRONTIER_LOCK_OK" in result.stdout

def test_promotion_obstruction_frontier_records_all_four_obstructions():
    data = json.loads(ART.read_text())
    assert data["recorded_obstruction_certificates"] == [
        "R1PromotionProofObstructionCertificate",
        "R2PromotionProofObstructionCertificate",
        "R3PromotionProofObstructionCertificate",
        "NonFactorisationBridgeProofObstructionCertificate",
    ]

def test_promotion_obstruction_frontier_closure_requires_elimination():
    data = json.loads(ART.read_text())
    assert data["frontier_state"] == "OPEN"
    assert data["closure_requires"] == [
        "R1PromotionProofObstructionEliminationCertificate",
        "R2PromotionProofObstructionEliminationCertificate",
        "R3PromotionProofObstructionEliminationCertificate",
        "NonFactorisationBridgeProofObstructionEliminationCertificate",
    ]

def test_promotion_obstruction_frontier_lean_has_no_target_closure():
    text = LEAN.read_text()
    assert "AllR1R2R3PromotionObstructionCertificatesRecorded" in text
    assert "R1R2R3PromotionObstructionFrontierClosureRequiresElimination" in text
    assert "theorem r1_promotion_proof_target :" not in text
    assert "theorem r2_promotion_proof_target :" not in text
    assert "theorem r3_promotion_proof_target :" not in text
    assert "theorem non_factorisation_bridge_proof_target :" not in text

def test_promotion_obstruction_frontier_boundary_blocks_overclaims():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "R1PromotionProofTarget" in blocked
    assert "R2PromotionProofTarget" in blocked
    assert "R3PromotionProofTarget" in blocked
    assert "NonFactorisationBridgeProofTarget" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "Chronos-RR" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
