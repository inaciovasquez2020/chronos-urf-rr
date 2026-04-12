from pathlib import Path

def test_newstein_root_to_vertex_path_concatenation_sublemma_locked():
    p = Path("docs/math/NEWSTEIN_ROOT_TO_VERTEX_PATH_CONCATENATION_SUBLEMMA.md")
    s = p.read_text()
    assert "# Newstein Root-to-Vertex Path Concatenation Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "the unique simple path from \\(r\\) to \\(v\\) is the concatenation of:" in s
    assert "the unique simple path from \\(r\\) to \\(\\operatorname{par}_T(v)\\)" in s
    assert "the edge \\((\\operatorname{par}_T(v),v)\\)" in s
    assert "## Proof skeleton" in s
    assert "This is the Step 2 input for the parent-depth decrement proof blueprint." in s
    assert "\\mathrm{RootToVertexPathConcatenation}" in s
    assert "\\mathrm{ParentDepthDecrement\\ proof}" in s
