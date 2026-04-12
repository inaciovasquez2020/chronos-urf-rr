from pathlib import Path

def test_newstein_direct_sum_independence_lock():
    s = Path("docs/math/NEWSTEIN_DIRECT_SUM_INDEPENDENCE_LEMMA.md").read_text()
    assert "# Newstein Direct-Sum Independence Lemma" in s
    assert "## Status\nOPEN" in s
    assert "hidden cross-fiber cancellation" in s
