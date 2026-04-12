from pathlib import Path

def test_newstein_next_step_registry_tracks_fiber_rank():
    s = Path("docs/status/NEWSTEIN_NEXT_STEP_REGISTRY.md").read_text()
    assert "Locked frontier" in s
    assert "TreeContractionHomotopy" in s
    assert "Conditional consequences already locked" in s
    assert "RootedBallTrivialization" in s
    assert "FiberQuotientRank" in s
