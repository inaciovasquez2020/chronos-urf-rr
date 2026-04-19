from pathlib import Path

def test_newstein_quotient_gap_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_QUOTIENT_GAP_THEOREM.md").read_text()
    assert "Status: OPEN" in s
    assert r"\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)\ge 2|V(X_n)|" in s
    assert r"\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)=\Omega(n)." in s
    assert "Rooted-ball trivialization theorem." in s
    assert "Fiber rank gap theorem." in s
    assert "Fiber-to-global direct-sum embedding." in s
