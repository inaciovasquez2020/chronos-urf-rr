from pathlib import Path

def test_newstein_fundamental_cycle_generation_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md").read_text()
    assert "# Newstein Fundamental Cycle Generation Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "every non-tree edge" in s
    assert "rooted-local generating family" in s
