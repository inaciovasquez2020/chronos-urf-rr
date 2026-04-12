from pathlib import Path

def test_newstein_next_step_registry_lock():
    s = Path("docs/status/NEWSTEIN_NEXT_STEP_REGISTRY.md").read_text()
    assert "# Newstein Next-Step Registry" in s
    assert "## Status\nOPEN" in s
    assert "NEWSTEIN_PARENT_DEPTH_DECREMENT_SUBLEMMA.md" in s
    assert "NEWSTEIN_ASSEMBLY_THEOREM.md" in s
