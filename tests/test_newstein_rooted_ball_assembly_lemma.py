from pathlib import Path

def test_newstein_rooted_ball_assembly_lemma_doc():
    s = Path("docs/math/NEWSTEIN_ROOTED_BALL_ASSEMBLY_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "\\phi_H(C)=0" in s
    assert "f_x:V(B_r^{B_n}(x))\\to\\mathbb F_2" in s
    assert "\\phi_H|_{B_r^{B_n}(x)}=\\delta f_x." in s
    assert "\\widetilde B_r^{\\,\\mathrm{tw}}(x)\\cong \\widetilde B_r^{\\,\\mathrm{triv}}(x)." in s
    assert "\\operatorname{Type}_{k,r}(G_n)=\\operatorname{Type}_{k,r}(H_n)." in s
    assert "No proof of the lemma is claimed here." in s
