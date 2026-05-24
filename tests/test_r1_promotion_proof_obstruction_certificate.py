import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/r1_promotion_proof_obstruction_certificate_2026_05_24.json"

def test_r1_promotion_obstruction_certificate_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_promotion_proof_obstruction_certificate.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_PROMOTION_PROOF_OBSTRUCTION_CERTIFICATE_OK" in result.stdout

def test_r1_counterexample_search_harness_target_passes():
    result = subprocess.run(
        [sys.executable, "tools/check_r1_promotion_counterexample_search_harness.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_PROMOTION_COUNTEREXAMPLE_SEARCH_HARNESS_TARGET_OK" in result.stdout

def test_r1_selected_target_remains_open():
    data = json.loads(ART.read_text())
    assert data["selected_target"] == "R1PromotionProofTarget"
    assert data["target_status"] == "OPEN"
    assert data["status"] == "R1_SELECTED_OBSTRUCTION_CERTIFICATE_OPEN"

def test_r1_obstruction_certificate_does_not_overclaim():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "R1PromotionProofTarget" in blocked
    assert "R1PromotionProofObstructionEliminationCertificate" in blocked
    assert "R1PromotionProofTargetReductionFromObstructionElimination" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
