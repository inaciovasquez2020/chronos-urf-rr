from pathlib import Path

def test_newstein_fiber_to_global_injection_lemma_lock():
    s = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTION_LEMMA.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in s
    assert "canonical comparison map" in s
    assert "is injective" in s
    assert "assembly theorem" in s
