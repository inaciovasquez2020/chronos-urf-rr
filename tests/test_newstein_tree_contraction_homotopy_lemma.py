from pathlib import Path

def test_newstein_tree_contraction_homotopy_lemma_lock():
    p = Path("docs/math/NEWSTEIN_TREE_CONTRACTION_HOMOTOPY_LEMMA.md")
    s = p.read_text()
    assert "## Status" in s
    assert "OPEN" in s
    assert "Weakest sufficient missing object" in s
    assert "support locality" in s.lower()
    assert "prism identity" in s.lower()
    assert "RootedBallTrivialization" in s
    assert "FiberQuotientRank" in s
