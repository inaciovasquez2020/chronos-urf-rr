from pathlib import Path

def test_newstein_non_tree_edge_fundamental_cycle_lemma_lock() -> None:
    s = Path("docs/math/NEWSTEIN_NON_TREE_EDGE_FUNDAMENTAL_CYCLE_LEMMA.md").read_text()
    assert "# Newstein Non-Tree-Edge Fundamental Cycle Lemma" in s
    assert "Status: PROVED" in s
    assert "## Status\nPROVED" in s
    assert "docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md" in s
    assert "docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md" in s
    assert "rooted-local fundamental cycle" in s
    assert "Closed by deduction from proved repository-native lemmas." in s
