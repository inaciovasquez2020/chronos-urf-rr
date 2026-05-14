from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FO4SemanticCompletenessToColapRankControl.lean").read_text()
status = Path("docs/status/CHRONOS_FO4_SEMANTIC_COMPLETENESS_TO_COLAP_RANK_CONTROL_2026_05_14.md").read_text()
artifact = json.loads(Path("artifacts/chronos/fo4_semantic_completeness_to_colap_rank_control_2026_05_14.json").read_text())

required_lean = [
    "def ColapRankControlFromSemanticCompleteness",
    "theorem semanticCompletenessToColapRankControl",
    "def FO4CycleOverlapRankBoundConditional",
    "theorem fo4CycleOverlapRankBoundConditional",
    "CONDITIONAL_COLAP_RANK_CONTROL_INTERFACE_CLOSED",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "CONDITIONAL_COLAP_RANK_CONTROL_INTERFACE_CLOSED"
assert artifact["closed_surface"] == "conditional semantic-completeness-to-ColapRankBoundedAt interface"

required_boundary = [
    "Conditional interface only.",
    "Rank control is repository-native ColapRankBoundedAt only.",
    "Does not prove graph-semantic ColapR rank control.",
    "Does not prove bounded cycle-overlap rank.",
    "Does not close rigidity.",
    "Does not prove P vs NP.",
    "Does not solve any Clay problem.",
]

for phrase in required_boundary:
    assert phrase in status, phrase

for forbidden in [
    "graph-semantic ColapR rank control is proved",
    "bounded cycle-overlap rank is proved",
    "rigidity is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("FO4 semantic-completeness-to-Colap-rank-control surface verified.")
