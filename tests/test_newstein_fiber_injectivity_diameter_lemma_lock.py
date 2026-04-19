from pathlib import Path

def test_newstein_fiber_injectivity_diameter_lemma_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FIBER_INJECTIVITY_DIAMETER_LEMMA.md").read_text()
    assert "# Newstein Fiber Injectivity Diameter Lemma" in s
    assert "Status: OPEN" in s
    assert r"\iota_u(c_u)=\iota_v(c_v)" in s
    assert r"\partial S=c_u-c_v" in s
    assert r"\operatorname{diam}(\operatorname{supp} S)>L" in s
    assert "weakest sufficient bridge from the local rank gap to the global direct-sum embedding" in s
