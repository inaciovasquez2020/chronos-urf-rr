from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FO4ColapROpenProblem.lean").read_text()
status = Path("docs/status/CHRONOS_FO4_COLAP_R_OPEN_PROBLEM_2026_05_14.md").read_text()
artifact = json.loads(Path("artifacts/chronos/fo4_colap_r_open_problem_2026_05_14.json").read_text())

required_lean = [
    "inductive F2",
    "structure RadiusRCycleWitness",
    "structure CycleOverlapIncidence",
    "structure F2WeightedOverlapRelation",
    "def ColapR",
    "def FO4CycleOverlapRankBoundProblem",
    "OPEN_PROBLEM_REQUIRED",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "OPEN_PROBLEM_REQUIRED"
assert artifact["closed_surface"] == "ColapR type surface over F2 formalized"
assert artifact["next_missing_object"] == "finite FO4 radius-R type enumeration under degree bound Delta"

required_boundary = [
    "Defines ColapR only.",
    "Does not prove finite FO4 radius-R type enumeration.",
    "Does not prove bounded cycle-overlap rank.",
    "Does not close rigidity.",
    "Does not prove P vs NP.",
    "Does not solve any Clay problem.",
]

for phrase in required_boundary:
    assert phrase in status, phrase

for forbidden in [
    "finite FO4 radius-R type enumeration is proved",
    "bounded cycle-overlap rank is proved",
    "rigidity is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("FO4 ColapR open-problem surface verified.")
