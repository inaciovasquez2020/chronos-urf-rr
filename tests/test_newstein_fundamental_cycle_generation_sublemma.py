from pathlib import Path

def test_newstein_fundamental_cycle_generation_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md").read_text()
    assert "# Newstein Fundamental Cycle Generation Sublemma" in s
    assert "## Status\nPROVED" in s
    assert "docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md" in s
    assert "docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md" in s
    assert "rooted-local generating family" in s
    assert "basis of \\(Z_1(L;\\mathbf F_2)\\)" in s or "form a basis of \\(Z_1(L;\\mathbf F_2)\\)" in s
