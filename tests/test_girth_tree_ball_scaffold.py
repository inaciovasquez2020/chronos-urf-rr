from pathlib import Path

def test_girth_tree_ball_scaffold_present():
    s = Path("URF/Lean/Local/GirthTreeBall.lean").read_text()
    assert "def InBall" in s
    assert "def BallAcyclic" in s
    assert "def GirthGT" in s
    assert "theorem girth_gt_twoR_implies_ball_acyclic" in s
