from pathlib import Path

def test_newstein_local_coboundary_criterion_doc():
    s = Path("docs/math/NEWSTEIN_LOCAL_COBOUNDARY_CRITERION.md").read_text()
    assert "Conditional target." in s
    assert "\\phi_H(C)=0" in s
    assert "f:V(U)\\to \\mathbb F_2" in s
    assert "\\phi_H|_U=\\delta f." in s
    assert "The local coboundary criterion implies rooted-ball trivialization." in s
    assert "No proof of the lemma is claimed here." in s
