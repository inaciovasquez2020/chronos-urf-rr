from pathlib import Path

def test_newstein_coboundary_assembly_lemma_doc():
    s = Path("docs/math/NEWSTEIN_COBOUNDARY_ASSEMBLY_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "\\phi(C)=0" in s
    assert "the Newstein cycle-difference lemma" in s
    assert "the Newstein edge-coboundary verification lemma" in s
    assert "f:V(U)\\to\\mathbb F_2" in s
    assert "\\phi=\\delta f." in s
    assert "The Newstein coboundary assembly lemma discharges the Newstein local coboundary criterion modulo the two isolated sublemmas." in s
    assert "No proof of the lemma is claimed here." in s
