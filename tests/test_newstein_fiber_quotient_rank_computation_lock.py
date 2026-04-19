from pathlib import Path

def test_newstein_fiber_quotient_rank_computation_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_COMPUTATION.md").read_text()
    assert "Status: OPEN" in s
    assert r"Z_1(\widetilde T)/W \cong H_1(\widetilde T;\mathbb F_2)" in s
    assert r"\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T^{\mathrm{triv}})/W^{\mathrm{triv}}\bigr)=4" in s
    assert r"\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T^{\mathrm{tw}})/W^{\mathrm{tw}}\bigr)=2" in s
    assert "Trivial cover is a disjoint union of two tori." in s
    assert "Chosen monodromy is odd on exactly one primitive torus direction." in s
    assert "Twisted cover is connected." in s
    assert "Lifted twisted fiber is a single torus." in s
