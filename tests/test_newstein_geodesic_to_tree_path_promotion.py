from pathlib import Path

def test_newstein_geodesic_to_tree_path_promotion_lock():
    s = Path("docs/math/NEWSTEIN_GEODESIC_TO_TREE_PATH_PROMOTION.md").read_text()
    assert "# Newstein Geodesic-to-Tree-Path Promotion" in s
    assert "## Status\nOPEN" in s
    assert "Tree-Path Rooted-Locality" in s or "Tree-Path Rooted-Locality Sublemma" in s
