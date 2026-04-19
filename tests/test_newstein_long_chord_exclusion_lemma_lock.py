from pathlib import Path

def test_newstein_long_chord_exclusion_lemma_lock() -> None:
    s = Path("docs/math/NEWSTEIN_LONG_CHORD_EXCLUSION_LEMMA.md").read_text()
    assert "# Newstein Long-Chord Exclusion Lemma" in s
    assert "Status: OPEN" in s
    assert r"\sigma_i=e_i+P_T(e_i)" in s
    assert r"e_i\notin \operatorname{supp}(w)" in s
    assert "weakest sufficient missing lemma for the proposed \\(\\sigma\\)-package" in s
    assert r"\dim_{\mathbf F_2}(W^{\mathrm{tw}}/W^{\mathrm{triv}})=2" in s
