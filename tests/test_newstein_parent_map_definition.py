from pathlib import Path

def test_newstein_parent_map_definition_lock():
    s = Path("docs/math/NEWSTEIN_PARENT_MAP_DEFINITION.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in s
    assert "Define the parent map" in s
    assert "unique-lower-neighbor property" in s
    assert "d(r,p(v))=d(r,v)-1" in s
    assert "rooted-tree certificate" in s
