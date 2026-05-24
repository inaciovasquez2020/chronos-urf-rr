from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/r1_long_chord_coherence_sufficiency_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/R1LongChordCoherenceSufficiency.lean")

def test_r1_long_chord_coherence_sufficiency_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_r1_long_chord_coherence_sufficiency.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R1_LONG_CHORD_COHERENCE_SUFFICIENCY_OK" in result.stdout

def test_r1_coherence_and_no_witness_are_defined():
    text = LEAN.read_text()
    assert "def RepositoryNativeR1LongChordCoherence" in text
    assert "def NoRepositoryNativeLongChordWitness" in text
    assert "∀ x : LongChordNativeObject" in text

def test_r1_coherence_blocks_witness_using_existing_contradiction():
    text = LEAN.read_text()
    assert "theorem repository_native_r1_long_chord_coherence_blocks_witness" in text
    assert "long_chord_witness_contradiction x hWitness (hCoherence x)" in text

def test_r1_promotion_elimination_target_is_not_proved():
    text = LEAN.read_text()
    assert "def R1LongChordCoherenceToPromotionObstructionEliminationTarget" in text
    assert "theorem r1_promotion_proof_obstruction_elimination_certificate" not in text

def test_r1_packet_records_remaining_missing_objects():
    data = json.loads(ART.read_text())
    assert "R1LongChordCoherenceToPromotionObstructionEliminationTarget proof" in data["still_missing_for_r1_elimination"]
    assert "R1PromotionProofObstructionEliminationCertificate" in data["still_missing_for_r1_elimination"]

def test_r1_packet_boundary_blocks_overclaims():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "R1PromotionProofObstructionEliminationCertificate" in blocked
    assert "R1PromotionProofTarget" in blocked
    assert "LongChordExclusion" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
