from pathlib import Path

def test_newstein_unique_lower_neighbor_lemma_lock():
    s = Path("docs/math/NEWSTEIN_UNIQUE_LOWER_NEIGHBOR_LEMMA.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in s
    assert "unique-lower-neighbor lemma" in s
    assert "B_R(r)" in s
    assert "d(r,u)=d(r,v)-1" in s
