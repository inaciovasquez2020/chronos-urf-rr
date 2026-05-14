from pathlib import Path

lean = Path("lean/Chronos/Frontier/FO4ColapRankControlToCycleOverlapRank.lean").read_text()
status = Path("docs/status/CHRONOS_FO4_COLAP_RANK_CONTROL_TO_CYCLE_OVERLAP_RANK_2026_05_14.md").read_text()
artifact = Path("artifacts/chronos/fo4_colap_rank_control_to_cycle_overlap_rank_2026_05_14.json").read_text()

required = [
    "PointwiseColapRankBoundsCycleOverlapRank",
    "ColapRankControlImpliesBoundedCycleOverlapRank",
    "colap_rank_control_implies_bounded_cycle_overlap_rank",
    "CycleOverlapRankBoundedAt",
    "CONDITIONAL_CYCLE_OVERLAP_RANK_INTERFACE_CLOSED",
    "Does not prove PointwiseColapRankBoundsCycleOverlapRank.",
    "Does not prove P vs NP.",
    "Does not solve any Clay problem.",
]

for token in required:
    assert token in lean or token in status or token in artifact, token

for forbidden in [
    "unconditional cycle-overlap-rank bound is proved",
    "rigidity closure is proved",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status
    assert forbidden not in artifact

print("FO4 Colap-rank-control to cycle-overlap-rank surface verified.")
