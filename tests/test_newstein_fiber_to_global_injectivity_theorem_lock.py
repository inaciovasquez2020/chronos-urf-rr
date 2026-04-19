from pathlib import Path

def test_newstein_fiber_to_global_injectivity_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTIVITY_THEOREM.md").read_text()
    assert "# Newstein Fiber to Global Injectivity Theorem" in s
    assert "Status: OPEN" in s
    assert r"\iota_v^{\mathrm{triv}}" in s
    assert r"\operatorname{im}(\iota_u)\cap \operatorname{im}(\iota_v)=0" in s
