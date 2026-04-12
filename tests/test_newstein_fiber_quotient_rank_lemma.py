from pathlib import Path

def test_newstein_fiber_quotient_rank_lemma_doc():
    s = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_LEMMA.md").read_text()
    assert "Conditional target." in s
    assert "\\dim_{\\mathbb F_2}\\!\\bigl(Z_1(\\widetilde T^{\\mathrm{triv}})/W^{\\mathrm{triv}}\\bigr)=4." in s
    assert "\\dim_{\\mathbb F_2}\\!\\bigl(Z_1(\\widetilde T^{\\mathrm{tw}})/W^{\\mathrm{tw}}\\bigr)=2." in s
    assert "two extra quotient-cycle classes" in s
    assert "No proof of the lemma is claimed here." in s
