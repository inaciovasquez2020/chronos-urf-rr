from pathlib import Path

def test_bounded_treewidth_decomposition_claim_present():
    p = Path("URF/Canonical/BoundedTreewidthDecompositionProperty.md")
    assert p.exists(), "missing canonical note"
    s = p.read_text()
    assert "bounded treewidth" in s.lower()
    assert "decomposition property" in s.lower()
    assert "Z_1(G)/Z_1^{≤ 2R+1}(G)" in s or "Z_1(G)/Z_1^{<= 2R+1}(G)" in s

def test_frontier_stub_present():
    p = Path("URF/Lean/Frontier/BoundedTreewidthDecomposition.lean")
    assert p.exists(), "missing Lean frontier file"
    s = p.read_text()
    assert "boundedTreewidthDecomposition" in s
