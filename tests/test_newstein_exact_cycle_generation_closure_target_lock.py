from pathlib import Path

def test_newstein_exact_cycle_generation_closure_target_lock() -> None:
    s = Path("docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md").read_text()
    assert "# Newstein Exact Cycle-Generation Closure Target" in s
    assert "Status: CONDITIONAL" in s
    assert "fundamental cycle" in s
    assert "rooted-local" in s
    assert "rooted-local generating family" in s or "spans" in s
    assert "Conditional consequence" in s
