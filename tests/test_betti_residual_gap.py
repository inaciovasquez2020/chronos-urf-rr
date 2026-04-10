from pathlib import Path

def test_betti_residual_gap_tokens():
    s = Path("URF/Lean/Graph/BettiResidualGap.lean").read_text()
    required = [
        "import URF.Lean.Graph.TreePathCycleBasis",
        "import URF.Lean.Graph.ComponentIndicatorBasis",
        "import URF.Lean.Graph.EdgeSpaceProjection",
        "theorem betti_residual_gap_shell_complete",
    ]
    for token in required:
        assert token in s, f"missing token: {token}"
