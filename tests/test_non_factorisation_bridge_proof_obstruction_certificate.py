from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/non_factorisation_bridge_proof_obstruction_certificate_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/NonFactorisationBridgeProofObstructionCertificate.lean")

def test_non_factorisation_bridge_obstruction_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_non_factorisation_bridge_proof_obstruction_certificate.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "NON_FACTORISATION_BRIDGE_PROOF_OBSTRUCTION_CERTIFICATE_OK" in result.stdout

def test_non_factorisation_bridge_counterexample_harness_target_passes():
    result = subprocess.run(
        ["python3", "tools/check_non_factorisation_bridge_counterexample_search_harness.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "NON_FACTORISATION_BRIDGE_COUNTEREXAMPLE_SEARCH_HARNESS_TARGET_OK" in result.stdout

def test_non_factorisation_bridge_artifact_keeps_target_open():
    data = json.loads(ART.read_text())
    assert data["selected_target"] == "NonFactorisationBridgeProofTarget"
    assert data["target_state"] == "OPEN"
    assert "NON_FACTORISATION_BRIDGE_OBSTRUCTION_ELIMINATION_PROOF" in data["next_missing_objects"]

def test_non_factorisation_bridge_depends_on_open_r1_r2_r3_targets():
    data = json.loads(ART.read_text())
    assert data["depends_on_open_targets"] == [
        "R1PromotionProofTarget",
        "R2PromotionProofTarget",
        "R3PromotionProofTarget",
    ]

def test_non_factorisation_bridge_lean_names_reduction_without_closing_target():
    text = LEAN.read_text()
    assert "def NonFactorisationBridgeProofTargetReductionFromObstructionElimination" in text
    assert "theorem non_factorisation_bridge_proof_target_reduction_from_obstruction_elimination" in text
    assert "theorem non_factorisation_bridge_proof_target :" not in text

def test_non_factorisation_bridge_boundary_blocks_overclaims():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "NonFactorisationBridgeProofTarget" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "Chronos-RR" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
