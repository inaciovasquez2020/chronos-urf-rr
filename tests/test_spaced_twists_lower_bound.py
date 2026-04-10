from pathlib import Path

def test_spaced_twists_proof_exists():
    p = Path("proofs/SPACED_TWISTS_LOWER_BOUND.md")
    assert p.exists()
    s = p.read_text()
    assert "I_URF" in s
    assert "≥ |M_n|" in s
