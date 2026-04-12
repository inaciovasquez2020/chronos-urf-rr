from pathlib import Path

def test_newstein_tree_path_to_fundamental_cycle_promotion_lock():
    s = Path("docs/math/NEWSTEIN_TREE_PATH_TO_FUNDAMENTAL_CYCLE_PROMOTION.md").read_text()
    assert "# Newstein Tree-Path-to-Fundamental-Cycle Promotion" in s
    assert "## Status\nOPEN" in s
    assert "rooted-local generating family" in s
