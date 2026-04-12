from pathlib import Path

def test_newstein_parent_on_root_to_vertex_path_sublemma_locked():
    p = Path("docs/math/NEWSTEIN_PARENT_ON_ROOT_TO_VERTEX_PATH_SUBLEMMA.md")
    s = p.read_text()
    assert "# Newstein Parent-on-Root-to-Vertex-Path Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "lies on the unique simple path from \\(r\\) to \\(v\\)." in s
    assert "## Proof skeleton" in s
    assert "This is the Step 1 input for the parent-depth decrement proof blueprint." in s
    assert "\\mathrm{ParentOnRootToVertexPath}" in s
    assert "\\mathrm{ParentDepthDecrement\\ proof}" in s
