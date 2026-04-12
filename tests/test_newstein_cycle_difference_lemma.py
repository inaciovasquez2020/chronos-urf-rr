from pathlib import Path

def test_newstein_cycle_difference_lemma_doc():
    s = Path("docs/math/NEWSTEIN_CYCLE_DIFFERENCE_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "P\\oplus Q" in s
    assert "is an \\(\\mathbb F_2\\)-cycle in \\(U\\)." in s
    assert "\\phi(C)=0" in s
    assert "\\sum_{e\\in P}\\phi(e)=\\sum_{e\\in Q}\\phi(e)." in s
    assert "The cycle-difference lemma supplies the path-independence step in the Newstein path-integration lemma." in s
    assert "No proof of the lemma is claimed here." in s
