from pathlib import Path


def test_newstein_fiber_quotient_rank_lemma_lock():
    text = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_LEMMA.md").read_text()
    assert "Status: PROVED" in text
    assert "quotient-rank 4 over F_2" in text
    assert "rank_F2(im(q_R restricted to fiber)) = 4." in text
    assert "Fiber Quotient-Rank Lemma" in text
