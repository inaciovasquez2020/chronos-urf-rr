from pathlib import Path

lean = Path("lean/Chronos/Frontier/FO4PointwiseColapToCycleOverlapRank.lean").read_text()
status = Path("docs/status/CHRONOS_FO4_POINTWISE_COLAP_TO_CYCLE_OVERLAP_RANK_2026_05_14.md").read_text()
artifact = Path("artifacts/chronos/fo4_pointwise_colap_to_cycle_overlap_rank_2026_05_14.json").read_text()

required = [
    "pointwise_colap_rank_bounds_cycle_overlap_rank",
    "colap_rank_control_implies_bounded_cycle_overlap_rank_closed",
    "PLACEHOLDER_SURFACE_CLOSED_ONLY",
    "Closes only the current placeholder surface",
    "Does not prove graph-semantic PointwiseColapRankBoundsCycleOverlapRank.",
    "Does not prove P vs NP.",
    "Does not solve any Clay problem.",
]

for token in required:
    assert token in lean or token in status or token in artifact, token

for forbidden in [
    "graph-semantic PointwiseColapRankBoundsCycleOverlapRank is proved",
    "unconditional graph-theoretic cycle-overlap-rank bound is proved",
    "rigidity closure is proved",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status
    assert forbidden not in artifact

print("FO4 pointwise Colap-to-cycle-overlap placeholder surface verified.")
