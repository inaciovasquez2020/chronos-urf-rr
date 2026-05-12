import subprocess
from pathlib import Path


def test_semantic_rank_defect_controls_entropy_defect_frontier_verifier():
    subprocess.run(
        ["python3", "tools/verify_semantic_rank_defect_controls_entropy_defect_frontier.py"],
        check=True,
    )


def test_semantic_rank_defect_controls_entropy_defect_frontier_lean_tokens():
    text = Path("Chronos/Frontier/SemanticRankDefectControlsEntropyDefectFrontier.lean").read_text()
    assert "structure NonPropRankEntropyData" in text
    assert "def SemanticRankDefectControlsEntropyDefectOn" in text
    assert "def WeakestMissingTheoremLevelInput" in text
    assert "def DirectRankEntropyTransferOn" in text
    assert "theorem conditional_rank_rate_gap_to_fiber_entropy_gap_from_direct_transfer" in text
    assert "admit" not in text
    assert "sorry" not in text
