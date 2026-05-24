from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/native_long_chord_diameter_capacity_ingredients_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/NativeLongChordDiameterCapacityIngredients.lean")

def test_native_ingredient_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_native_long_chord_diameter_capacity_ingredients.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "NATIVE_LONG_CHORD_DIAMETER_CAPACITY_INGREDIENTS_OK" in result.stdout

def test_long_chord_native_objects_are_defined():
    text = LEAN.read_text()
    assert "structure LongChordEndpoint" in text
    assert "structure LongChordMetricDatum" in text
    assert "structure LongChordNativeObject" in text
    assert "def LongChordWitness" in text
    assert "def NativeLongChordCoherence" in text

def test_long_chord_contradiction_lemma_is_present():
    text = LEAN.read_text()
    assert "theorem long_chord_witness_contradiction" in text
    assert "False" in text
    assert "Nat.lt_of_lt_of_le" in text

def test_diameter_filling_invariant_and_lower_bound_are_present():
    text = LEAN.read_text()
    assert "structure DiameterFillingNativeObject" in text
    assert "def DiameterFillingCompatibility" in text
    assert "theorem monotone_separation_lower_bound" in text
    assert "Nat.le_trans" in text

def test_explicit_capacity_bound_c_is_defined():
    data = json.loads(ART.read_text())
    text = LEAN.read_text()
    assert data["explicit_capacity_bound_C"] == 4096
    assert "def ExplicitLocalTypeCapacityC : Nat :=" in text
    assert "4096" in text
    assert "theorem local_type_capacity_bound_certificate" in text

def test_packet_does_not_claim_obstruction_elimination():
    data = json.loads(ART.read_text())
    assert "R1PromotionProofObstructionEliminationCertificate" in data["still_missing_for_obstruction_elimination"]
    assert "R2PromotionProofObstructionEliminationCertificate" in data["still_missing_for_obstruction_elimination"]
    assert "R3PromotionProofObstructionEliminationCertificate" in data["still_missing_for_obstruction_elimination"]
    assert "NonFactorisationBridgeProofObstructionEliminationCertificate" in data["still_missing_for_obstruction_elimination"]

def test_packet_boundary_blocks_overclaims():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "LongChordExclusion" in blocked
    assert "DiameterSeparationFillingObstruction" in blocked
    assert "UniformLocalTypeCapacity" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
