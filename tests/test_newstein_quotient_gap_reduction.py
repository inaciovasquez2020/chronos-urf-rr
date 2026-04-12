from pathlib import Path

def test_newstein_quotient_gap_reduction_doc():
    p = Path("docs/math/NEWSTEIN_QUOTIENT_GAP_REDUCTION.md")
    s = p.read_text()

    assert "Conditional reduction only." in s
    assert "Fiber Quotient-Rank Lemma" in s
    assert "\\dim_{\\mathbb F_2}\\!\\bigl(Z_1(\\widetilde T_v^{\\mathrm{triv}})/W_v^{\\mathrm{triv}}\\bigr)=4" in s
    assert "\\dim_{\\mathbb F_2}\\!\\bigl(Z_1(\\widetilde T_v^{\\mathrm{tw}})/W_v^{\\mathrm{tw}}\\bigr)=2" in s
    assert "No full proof of the \\(\\Omega(n)\\) quotient-gap theorem is claimed here." in s
