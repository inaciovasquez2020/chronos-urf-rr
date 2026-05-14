from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FO4HomogeneousOpenProblem.lean").read_text()
status = Path("docs/status/CHRONOS_FO4_HOMOGENEOUS_OPEN_PROBLEM_2026_05_14.md").read_text()
artifact = json.loads(Path("artifacts/chronos/fo4_homogeneous_open_problem_2026_05_14.json").read_text())

required = [
    "structure FO4HomogeneousInput",
    "def FO4Homogeneous",
    "OPEN_PROBLEM_REQUIRED",
    "FO4-local indistinguishability",
]

for token in required:
    assert token in lean or token in status, token

assert artifact["status"] == "OPEN_PROBLEM_REQUIRED"
assert artifact["next_missing_object"] == "Colap_R(G) over F2"

for forbidden in [
    "bounded cycle-overlap rank is proved",
    "rigidity is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("FO4Homogeneous open-problem surface verified.")
