from pathlib import Path

def test_newstein_tree_path_rooted_locality_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_TREE_PATH_ROOTED_LOCALITY_SUBLEMMA.md").read_text()
    assert "# Newstein Tree-Path Rooted-Locality Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "unique tree path" in s
    assert "rooted-local radius regime" in s
