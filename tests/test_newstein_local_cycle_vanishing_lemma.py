from pathlib import Path

def test_newstein_local_cycle_vanishing_lemma_doc():
    s = Path("docs/math/NEWSTEIN_LOCAL_CYCLE_VANISHING_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "\\phi_H(C)=0." in s
    assert "generated over \\(\\mathbb F_2\\) by local triangle boundaries" in s
    assert "\\phi_H(\\partial\\tau)=0" in s
    assert "The local cycle-vanishing lemma discharges the remaining hypothesis of the Newstein rooted-ball assembly lemma." in s
    assert "No proof of the lemma is claimed here." in s
