from pathlib import Path

def test_newstein_triangle_vanishing_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_TRIANGLE_VANISHING_THEOREM.md").read_text()
    assert "Status: OPEN" in s
    assert r"\phi_H(\partial\tau)=0" in s
    assert "Explicit cocycle definition on every edge class." in s
    assert "Direct parity check on each triangle type." in s
    assert r"Additivity of \(\phi_H\) on \(\mathbb F_2\)-boundary sums." in s
