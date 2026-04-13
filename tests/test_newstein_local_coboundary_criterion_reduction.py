from pathlib import Path

def test_newstein_local_coboundary_criterion_reduction_lock() -> None:
    text = Path("docs/math/NEWSTEIN_LOCAL_COBOUNDARY_CRITERION_REDUCTION.md").read_text(encoding="utf-8")
    assert "Status: PROVED" in text
    assert "\\forall z \\in Z_1(B_R(r);\\mathbf F_2)" in text
    assert "\\exists c \\in C_2(B_R(r);\\mathbf F_2)" in text
    assert "\\partial c = z" in text
    assert "every local \\(1\\)-cycle is a local boundary" in text
    assert "LocalCoboundaryCriterion is reduced to RootedBallTrivialization." in text
    assert "Proved from RootedBallTrivialization." in text
