from pathlib import Path

def test_newstein_next_step_registry_tracks_tree_homotopy():
    p = Path("docs/status/NEWSTEIN_NEXT_STEP_REGISTRY.md")
    s = p.read_text()
    assert "Current frontier" in s
    assert "TreeContractionHomotopy" in s
    assert "Proof closure is not 100% until `TreeContractionHomotopy` is formalized or explicitly assumed." in s
