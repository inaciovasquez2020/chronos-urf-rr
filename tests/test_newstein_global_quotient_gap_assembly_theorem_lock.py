from pathlib import Path

def test_newstein_global_quotient_gap_assembly_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_GLOBAL_QUOTIENT_GAP_ASSEMBLY_THEOREM.md").read_text()
    assert "# Newstein Global Quotient Gap Assembly Theorem" in s
    assert "Status: OPEN" in s
    assert r"\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)\ge 2|V(X_n)|" in s
    assert r"\Omega(n)" in s
