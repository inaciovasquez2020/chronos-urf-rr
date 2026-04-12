from pathlib import Path

def test_newstein_fiber_to_global_injection_lock():
    s = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTION_LEMMA.md").read_text()
    assert "# Newstein Fiber-to-Global Injection Lemma" in s
    assert "## Status\nOPEN" in s
    assert "\\ker(\\Phi)=0" in s
