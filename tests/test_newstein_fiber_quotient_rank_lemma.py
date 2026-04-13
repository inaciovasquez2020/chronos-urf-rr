from pathlib import Path


def test_newstein_fiber_quotient_rank_lock():
    s = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_LEMMA.md").read_text()
    assert "# Newstein Fiber Quotient-Rank Lemma" in s
    assert "Status: OPEN" in s
    assert "quotient-rank 4 over F_2" in s
    assert "rank_F2(im(q_R restricted to fiber)) = 4." in s
