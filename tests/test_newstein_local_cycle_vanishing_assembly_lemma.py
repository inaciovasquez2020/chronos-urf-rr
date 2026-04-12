from pathlib import Path

def test_newstein_local_cycle_vanishing_assembly_lemma_doc():
    s = Path("docs/math/NEWSTEIN_LOCAL_CYCLE_VANISHING_ASSEMBLY_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "the Newstein local triangle-generation lemma" in s
    assert "the Newstein triangle-vanishing lemma" in s
    assert "\\phi_H(C)=0." in s
    assert "The Newstein local cycle-vanishing assembly lemma discharges the Newstein local cycle-vanishing lemma from its two isolated sublemmas." in s
    assert "No proof of the lemma is claimed here." in s
