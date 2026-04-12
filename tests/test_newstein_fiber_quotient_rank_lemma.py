from pathlib import Path

def test_newstein_fiber_quotient_rank_lock():
    s = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_LEMMA.md").read_text()
    assert "# Newstein Fiber Quotient-Rank Lemma" in s
    assert "## Status\nOPEN" in s
    assert "r_\\ast \\in \\{2,4\\}" in s or "r_\\ast \\in \\{2,4\\}." in s
