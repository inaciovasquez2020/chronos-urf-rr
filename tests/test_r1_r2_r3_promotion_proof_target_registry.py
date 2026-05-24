import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/r1_r2_r3_promotion_proof_target_registry_2026_05_24.json"

def test_promotion_proof_target_registry_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_r2_r3_promotion_proof_target_registry.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_R2_R3_PROMOTION_PROOF_TARGET_REGISTRY_OK" in result.stdout

def test_registry_has_four_open_targets():
    data = json.loads(ART.read_text())
    names = [item["name"] for item in data["open_targets"]]
    assert names == [
        "R1PromotionProofTarget",
        "R2PromotionProofTarget",
        "R3PromotionProofTarget",
        "NonFactorisationBridgeProofTarget",
    ]
    assert all(item["status"] == "OPEN" for item in data["open_targets"])

def test_registry_does_not_overclaim():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "R1PromotionProofTarget" in blocked
    assert "R2PromotionProofTarget" in blocked
    assert "R3PromotionProofTarget" in blocked
    assert "NonFactorisationBridgeProofTarget" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
