from pathlib import Path

def test_newstein_rooted_ball_trivialization_lock():
text = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION.md").read_text()
assert "Status: OPEN" in text
assert "every supported 1-cycle is null-homologous inside the same rooted ball" in text
assert "forall z \in Z_1(B_R(r))" not in text
assert "For every rooted ball" in text

def test_newstein_frontier_status_tracks_rooted_ball_trivialization():
text = Path("docs/status/NEWSTEIN_FRONTIER_STATUS.md").read_text()
assert "Status: CONDITIONAL" in text
assert "Remaining weakest theorem-level object:" in text
assert "- RootedBallTrivialization" in text
assert "TreeContractionHomotopy placeholder -> proof" in text
