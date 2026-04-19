from pathlib import Path

def test_newstein_exact_cycle_generation_closure_target_lock() -> None:
    s = Path("docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md").read_text()
    assert "# Newstein Exact Cycle-Generation Closure Target" in s
    assert "fundamental cycle" in s
    assert "rooted-local" in s
    assert "rooted-local generating family" in s
    assert "spans" in s or "generates the full local cycle space" in s

def test_newstein_open_files_cite_closure_target() -> None:
    targets = [
        "docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md",
        "docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_PROOF_BLUEPRINT.md",
        "docs/math/NEWSTEIN_NON_TREE_EDGE_FUNDAMENTAL_CYCLE_LEMMA.md",
    ]
    for path in targets:
        s = Path(path).read_text()
        assert "docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md" in s
