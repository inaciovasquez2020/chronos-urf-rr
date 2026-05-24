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

def test_r2_compatibility_and_lower_bound_are_defined():
    text = LEAN.read_text()
    assert "def RepositoryNativeR2DiameterFillingCompatibility" in text
    assert "def RepositoryNativeR2SeparationLowerBound" in text
    assert "∀ x : DiameterFillingNativeObject" in text

def test_r2_compatibility_gives_lower_bound_using_existing_lemma():
    text = LEAN.read_text()
    assert "theorem repository_native_r2_diameter_filling_compatibility_gives_lower_bound" in text
    assert "monotone_separation_lower_bound x (hCompat x)" in text

def test_r2_promotion_elimination_target_is_not_proved():
    text = LEAN.read_text()
    assert "def R2DiameterFillingCompatibilityToPromotionObstructionEliminationTarget" in text
    assert "theorem r2_promotion_proof_obstruction_elimination_certificate" not in text

def test_r2_packet_records_remaining_missing_objects():
    data = json.loads(ART.read_text())
    assert "R2DiameterFillingCompatibilityToPromotionObstructionEliminationTarget proof" in data["still_missing_for_r2_elimination"]
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
