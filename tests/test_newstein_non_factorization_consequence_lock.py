from pathlib import Path

def test_newstein_non_factorization_consequence_lock() -> None:
    s = Path("docs/math/NEWSTEIN_NON_FACTORIZATION_CONSEQUENCE.md").read_text()
    assert "Status: OPEN" in s
    assert r"\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n)" in s
    assert r"Q(G_n)\neq Q(H_n)" in s
    assert "does not factor through rooted radius-\\(r\\) type or \\(FO^k_r\\)-type" in s
    assert "Rooted-ball trivialization theorem." in s
    assert "Quotient-gap theorem." in s
    assert "Definition of the quotient invariant \\(Q\\)." in s
    assert "Factorization contradiction argument." in s
