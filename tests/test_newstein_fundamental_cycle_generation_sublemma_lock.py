from pathlib import Path

def test_newstein_fundamental_cycle_generation_sublemma_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md").read_text()
    assert "# Newstein Fundamental Cycle Generation Sublemma" in s
    assert "Status: PROVED" in s
    assert "## Target statement" in s
    assert "## Exact closure target" in s
    assert "## Deduction target" in s
    assert "docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md" in s
    assert "docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md" in s
    assert "## Status" in s
    assert "Closed by deduction from proved repository-native lemmas." in s
    assert "## Finish condition" in s
