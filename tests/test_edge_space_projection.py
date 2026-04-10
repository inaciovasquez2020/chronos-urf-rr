from pathlib import Path

def test_edge_space_projection_tokens():
    s = Path("URF/Lean/Graph/EdgeSpaceProjection.lean").read_text()
    required = [
        "structure CycleProjection",
        "structure CutProjection",
        "theorem cycle_projection_well_defined",
        "theorem cut_projection_well_defined",
        "theorem edge_vector_decomposes",
        "theorem cycle_cut_split_direct",
    ]
    for token in required:
        assert token in s, f"missing token: {token}"
