from pathlib import Path

def test_betti_number_target_present():
    s = Path("docs/specs/BETTI_NUMBER_TARGET.md").read_text()
    assert "Open problem." in s
    assert "\\beta_1(G)=\\dim_{\\mathbf F_2} Z_1(G)=|E|-|V|+c(G)." in s
    assert "No placeholder Lean theorem should be committed" in s
