from pathlib import Path

def test_newstein_parent_depth_length_identity_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_PARENT_DEPTH_LENGTH_IDENTITY_SUBLEMMA.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in s
    assert "parent-depth-length identity" in s
    assert "d(r,v)-1" in s
    assert "rooted-tree certificate" in s
