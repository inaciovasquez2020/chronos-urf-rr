from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/r2_diameter_filling_compatibility_sufficiency_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/R2DiameterFillingCompatibilitySufficiency.lean")

def test_r2_diameter_filling_compatibility_sufficiency_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_r2_diameter_filling_compatibility_sufficiency.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R2_DIAMETER_FILLING_COMPATIBILITY_SUFFICIENCY_OK" in result.stdout

def test_r2_cross_root_face_incidence_package_is_defined():
    text = LEAN.read_text()
    assert "def RepositoryNativeR2CrossRootFaceIncidence" in text
    assert "∀ chain : R2IncidenceFaceChain" in text
    assert "R2CrossRootFaceIncidenceObstruction chain" in text

def test_r2_cross_root_face_incidence_theorem_uses_packet_obstruction():
    text = LEAN.read_text()
    assert "theorem repository_native_r2_cross_root_face_incidence" in text
    assert "r2_cross_root_face_incidence_obstruction" in text

def test_r2_cross_root_promotion_elimination_target_is_not_proved():
    text = LEAN.read_text()
    assert "def R2CrossRootFaceIncidenceToPromotionObstructionEliminationTarget" in text
    assert "theorem r2_promotion_proof_obstruction_elimination_certificate" not in text

def test_r2_packet_records_remaining_missing_objects():
    data = json.loads(ART.read_text())
    assert "R2CrossRootFaceIncidenceToPromotionObstructionEliminationTarget proof" in data["still_missing_for_r2_elimination"]
    assert "R2PromotionProofObstructionEliminationCertificate" in data["still_missing_for_r2_elimination"]

def test_r2_packet_boundary_blocks_overclaims():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "R2PromotionProofObstructionEliminationCertificate" in blocked
    assert "R2PromotionProofTarget" in blocked
    assert "DiameterSeparationFillingObstruction" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
