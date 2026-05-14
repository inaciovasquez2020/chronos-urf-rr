from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FO4CycleOverlapOpenProblemRequired.lean").read_text()
doc = Path("docs/status/FO4_CYCLE_OVERLAP_OPEN_PROBLEM_REQUIRED_2026_05_14.md").read_text()
artifact = json.loads(
    Path("artifacts/chronos/fo4_cycle_overlap_open_problem_required_2026_05_14.json").read_text()
)

required_lean = [
    "structure FO4GraphSemanticRankInput where",
    "def GraphSemanticCycleOverlapRankDominatedByColapRank : Prop :=",
    "def counterexample : FO4GraphSemanticRankInput :=",
    "theorem unrestricted_graph_semantic_cycle_overlap_dominated_false",
    "structure FO4GraphSemanticRankInputRestricted where",
    "cycleOverlap_le_colap : cycleOverlapRank ≤ colapRank",
    "theorem restricted_graph_semantic_cycle_overlap_dominated_closed",
    "open_problem_required",
]

required_doc = [
    "Status: OPEN_PROBLEM_REQUIRED",
    "It is false under the current unrestricted structure.",
    "{ Delta := 0, R := 0, colapRank := 0, cycleOverlapRank := 1 }",
    "No unconditional graph-theoretic cycle-overlap rank bound is proved.",
    "No rigidity closure is proved.",
    "No P vs NP closure is proved.",
    "No Clay-problem closure is proved.",
]

for phrase in required_lean:
    assert phrase in lean, phrase

for phrase in required_doc:
    assert phrase in doc, phrase

assert artifact["status"] == "OPEN_PROBLEM_REQUIRED"
assert artifact["counterexample"]["colapRank"] == 0
assert artifact["counterexample"]["cycleOverlapRank"] == 1

for forbidden in [
    "unconditional graph-theoretic cycle-overlap rank bound is proved",
    "rigidity closure is proved",
    "P vs NP closure is proved",
    "Clay-problem closure is proved",
]:
    assert forbidden not in doc.replace("No " + forbidden, ""), forbidden

print("FO4 cycle-overlap OPEN_PROBLEM_REQUIRED surface verified.")
