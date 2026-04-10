from pathlib import Path

def test_bounded_treewidth_proof_exists():
    p = Path("proofs/BOUNDED_TREEWIDTH_DECOMPOSITION_PROOF.md")
    assert p.exists()
    s = p.read_text()
    assert "treewidth" in s.lower()
    assert "decomposition" in s.lower()
