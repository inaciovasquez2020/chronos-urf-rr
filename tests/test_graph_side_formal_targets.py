from pathlib import Path

def test_graph_side_targets_are_fixed():
    s = Path("docs/specs/GRAPH_SIDE_FORMAL_TARGETS.md").read_text()
    assert "I_R(G)" in s
    assert "Theorem A" in s
    assert "Theorem B" in s
    assert "Theorem C" in s
    assert "conditional until exact formal definitions are fixed" in s
    assert "formal definition of \\(ED(P_n)\\)" in s
