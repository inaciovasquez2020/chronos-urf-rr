from pathlib import Path

def test_newstein_proof_closure_status_tracks_rooted_ball_as_conditional():
    s = Path("docs/status/NEWSTEIN_PROOF_CLOSURE_STATUS.md").read_text()
    assert "Locked frontier" in s
    assert "TreeContractionHomotopy" in s
    assert "Immediate conditional consequence" in s
    assert "RootedBallTrivialization" in s
    assert "conditional on the formal existence of the local contraction homotopy" in s
