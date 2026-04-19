from pathlib import Path

def test_newstein_local_triangle_generation_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_LOCAL_TRIANGLE_GENERATION_THEOREM.md").read_text()
    assert "Status: OPEN" in s
    assert r"Z_1\!\bigl(B_r^{B_n}(x)\bigr)" in s
    assert "no radius-\\(r\\) ball wraps around a torus fiber" in s
    assert "no radius-\\(r\\) ball contains a backbone cycle" in s
    assert "local \\(2\\)-complex is simply connected" in s
    assert "Every local \\(\\mathbb F_2\\)-cycle is a sum of triangle boundaries." in s
