from pathlib import Path

def test_newstein_fiber_to_global_injection_reduction_lock() -> None:
    text = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTION_REDUCTION.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in text
    assert "\\forall z \\in Z_1(B_R(r);\\mathbf F_2)" in text
    assert "\\exists c \\in C_2(B_R(r);\\mathbf F_2)" in text
    assert "\\gamma = \\partial C" in text
    assert "\\partial c = \\gamma" in text
    assert "a contradiction" in text
    assert "FiberToGlobalInjection is reduced to the local coboundary criterion plus restriction of global boundaries to the supporting rooted ball." in text
