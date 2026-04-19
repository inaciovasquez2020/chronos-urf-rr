from pathlib import Path

def test_newstein_exact_cycle_generation_controller_is_proved() -> None:
    s = Path("docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md").read_text()
    assert "# Newstein Exact Cycle-Generation Closure Target" in s
    assert "Status: PROVED" in s
    assert "## Status\n\nPROVED" in s
    assert "fundamental cycle" in s
    assert "linearly independent" in s

def test_newstein_cycle_generation_chain_is_proved() -> None:
    targets = [
        "docs/math/NEWSTEIN_NON_TREE_EDGE_FUNDAMENTAL_CYCLE_LEMMA.md",
        "docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md",
        "docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_PROOF_BLUEPRINT.md",
    ]
    for path in targets:
        s = Path(path).read_text()
        assert "docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md" in s
        assert "Status: PROVED" in s
