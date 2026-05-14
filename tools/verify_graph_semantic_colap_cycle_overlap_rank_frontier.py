from pathlib import Path

lean = Path("lean/Chronos/Frontier/GraphSemanticColapCycleOverlapRankFrontier.lean").read_text()
status = Path("docs/status/CHRONOS_GRAPH_SEMANTIC_COLAP_CYCLE_OVERLAP_RANK_FRONTIER_2026_05_14.md").read_text()
artifact = Path("artifacts/chronos/graph_semantic_colap_cycle_overlap_rank_frontier_2026_05_14.json").read_text()

required = [
    "FO4GraphSemanticRankInput",
    "GraphSemanticFO4ColapRankBoundedAt",
    "GraphSemanticCycleOverlapRankBoundedAt",
    "GraphSemanticCycleOverlapRankDominatedByColapRank",
    "graph_semantic_pointwise_colap_rank_bounds_cycle_overlap_rank",
    "graph_semantic_colap_rank_control_implies_bounded_cycle_overlap_rank_from_domination",
    "CONDITIONAL_GRAPH_SEMANTIC_NUMERIC_FRONTIER",
    "Does not prove GraphSemanticCycleOverlapRankDominatedByColapRank.",
    "Does not prove P vs NP.",
    "Does not solve any Clay problem.",
]

for token in required:
    assert token in lean or token in status or token in artifact, token

for forbidden in [
    "GraphSemanticCycleOverlapRankDominatedByColapRank is proved",
    "unconditional graph-theoretic cycle-overlap-rank bound is proved",
    "rigidity closure is proved",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status
    assert forbidden not in artifact

print("Graph-semantic Colap/cycle-overlap rank frontier verified.")
