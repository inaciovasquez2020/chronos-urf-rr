from pathlib import Path

def test_newstein_non_tree_edge_fundamental_cycle_lemma_lock() -> None:
    s = Path("docs/math/NEWSTEIN_NON_TREE_EDGE_FUNDAMENTAL_CYCLE_LEMMA.md").read_text()
    assert "# Newstein Non-Tree-Edge Fundamental Cycle Lemma" in s
    assert "Status: OPEN" in s
    assert "## Status\nOPEN" in s
    assert "Fix a spanning tree in the rooted local complex." in s
    assert "For every non-tree edge" in s
    assert "### 1. Local spanning-tree choice" in s
    assert "### 2. Unique path property" in s
    assert "### 3. Fundamental cycle definition" in s
    assert "### 4. Rooted locality" in s
    assert "### 5. Generating role" in s
    assert "rooted-local generating family" in s
    assert "weakest missing sublemma" in s
