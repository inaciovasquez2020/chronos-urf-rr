def test_tree_path_cycle_basis_tokens():
    from pathlib import Path

    P = Path("URF/Lean/Graph/TreePathCycleBasis.lean")
    s = P.read_text()

    required = [
        "structure SpanningForest",
        "structure ParentMap",
        "structure TreePath",
        "structure FundamentalCycle",
        "def pathOp",
        "def fundamentalCycle",
        "theorem kernel_decomposes_into_fundamental_cycles",
        "theorem fundamental_cycles_independent",
        "theorem component_indicators_span_cokernel",
        "theorem edge_space_cycle_cut_split",
    ]

    for token in required:
        assert token in s, f"missing token: {token}"
