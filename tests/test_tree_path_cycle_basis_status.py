from pathlib import Path

def test_tree_path_cycle_basis_status_tokens():
    s = Path("URF/Lean/Graph/TreePathCycleBasis.lean").read_text()
    assert "theorem kernel_decomposes_into_fundamental_cycles" in s
    assert "theorem fundamental_cycles_independent" in s
    assert "theorem component_indicators_span_cokernel" in s
    assert "theorem edge_space_cycle_cut_split" in s
