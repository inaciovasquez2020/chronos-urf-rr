from pathlib import Path

def test_newstein_rooted_local_tree_path_lemma_lock() -> None:
    s = Path("docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md").read_text()
    assert "# Newstein Rooted-Local Tree-Path Lemma" in s
    assert "Status: OPEN" in s
    assert "unique tree path" in s
    assert "rooted-local" in s
    assert "minimal repository-native lemma" in s
