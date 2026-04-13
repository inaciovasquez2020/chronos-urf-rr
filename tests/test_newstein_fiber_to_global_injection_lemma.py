from pathlib import Path


def test_newstein_fiber_to_global_injection_lock():
    s = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTION_LEMMA.md").read_text()
    assert "# Newstein Fiber-to-Global Injection Lemma" in s
    assert "Status: OPEN" in s
    assert "canonical map from the surviving fiber quotient classes into the global quotient is injective" in s
    assert "maps to 0 in the global quotient" in s
    assert "already 0 in the fiber quotient" in s
