from pathlib import Path

def test_newstein_quotient_gap_assembly_theorem_doc():
    s = Path("docs/math/NEWSTEIN_QUOTIENT_GAP_ASSEMBLY_THEOREM.md").read_text()
    assert "Conditional target." in s
    assert "\\operatorname{Type}_{k,r}(G_n)=\\operatorname{Type}_{k,r}(H_n)" in s
    assert "\\dim_{\\mathbb F_2} Q(G_n)-\\dim_{\\mathbb F_2} Q(H_n)\\ge 2|V(X_n)|." in s
    assert "\\dim_{\\mathbb F_2} Q(G_n)-\\dim_{\\mathbb F_2} Q(H_n)=\\Omega(n)." in s
    assert "T_n \\ge \\frac{2|V(X_n)|}{C}." in s
    assert "No proof of the theorem is claimed here." in s
