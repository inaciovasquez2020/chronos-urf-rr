from pathlib import Path

def test_newstein_triangle_vanishing_lemma_doc():
    s = Path("docs/math/NEWSTEIN_TRIANGLE_VANISHING_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "\\phi_H(\\partial\\tau)=0." in s
    assert "Together with the Newstein local triangle-generation lemma" in s
    assert "\\phi_H(C)=0" in s
    assert "hence the Newstein local cycle-vanishing lemma." in s
    assert "No proof of the lemma is claimed here." in s
