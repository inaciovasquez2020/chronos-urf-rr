import json
from pathlib import Path

ART = Path("artifacts/chronos/gravity_pull_push_actual_value_test_2026_05_28.json")
DOC = Path("docs/status/GRAVITY_PULL_PUSH_ACTUAL_VALUE_TEST_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/GravityPullPushActualValueTest.lean")
ROOT = Path("lean/Chronos.lean")

required_boundaries = [
    "physical repulsive gravity",
    "new gravitational force law",
    "Einstein-matter PDE well-posedness",
    "collapse theorem",
    "black-hole formation theorem",
    "cosmic censorship",
    "hoop conjecture",
    "dark matter replacement",
    "gravity closure",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
]

required_lean_tokens = [
    "structure GravityPullPushSample",
    "def pullResidual",
    "def pushResidual",
    "def totalMagnitude",
    "empty_pull_push_actual_values",
    "balanced_pull_push_actual_values",
    "pull_dominant_actual_values",
    "push_dominant_actual_values",
    "pullResidual pullDominantWitness = 8",
    "pushResidual pushDominantWitness = 5",
]

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
root = ROOT.read_text()

assert data["status"] == "FINITE_ACTUAL_VALUE_ACCOUNTING_TEST_ONLY"
assert data["object"] == "GravityPullPushActualValueTest"
assert "import Chronos.Frontier.GravityPullPushActualValueTest" in root

actual = data["actual_values"]
assert actual["empty"]["totalMagnitude"] == 0
assert actual["balanced"]["pullMagnitude"] == 7
assert actual["balanced"]["pushMagnitude"] == 7
assert actual["balanced"]["totalMagnitude"] == 14
assert actual["pull_dominant"]["pullMagnitude"] == 13
assert actual["pull_dominant"]["pushMagnitude"] == 5
assert actual["pull_dominant"]["pullResidual"] == 8
assert actual["pull_dominant"]["pushResidual"] == 0
assert actual["pull_dominant"]["totalMagnitude"] == 18
assert actual["push_dominant"]["pullMagnitude"] == 4
assert actual["push_dominant"]["pushMagnitude"] == 9
assert actual["push_dominant"]["pullResidual"] == 0
assert actual["push_dominant"]["pushResidual"] == 5
assert actual["push_dominant"]["totalMagnitude"] == 13

for token in required_lean_tokens:
    assert token in lean, token

for token in required_boundaries:
    assert token in data["does_not_prove"], token
    assert token in doc, token

print("GRAVITY_PULL_PUSH_ACTUAL_VALUE_TEST_OK")
