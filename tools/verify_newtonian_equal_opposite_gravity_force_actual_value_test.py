import json
from pathlib import Path

ART = Path("artifacts/chronos/newtonian_equal_opposite_gravity_force_actual_value_test_2026_05_28.json")
DOC = Path("docs/status/NEWTONIAN_EQUAL_OPPOSITE_GRAVITY_FORCE_ACTUAL_VALUE_TEST_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/NewtonianEqualOppositeGravityForceActualValueTest.lean")
ROOT = Path("lean/Chronos.lean")

required_boundaries = [
    "new gravitational force law",
    "physical repulsive gravity",
    "relativistic Einstein equation",
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
    "structure NewtonianTwoBodySample",
    "def commonForceMagnitude",
    "def forceOnAByB",
    "def forceOnBByA",
    "def equalAndOppositeForces",
    "equal_opposite_force_identity",
    "actual_earth_moon_scaled_force_values",
    "actual_balanced_unit_force_values",
    "forceOnAByB actualEarthMoonScaledWitness = -36",
    "forceOnBByA actualEarthMoonScaledWitness = 36",
    "forceOnAByB actualBalancedUnitWitness = -30",
    "forceOnBByA actualBalancedUnitWitness = 30",
]

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
root = ROOT.read_text()

assert data["status"] == "FINITE_NEWTONIAN_ACTUAL_VALUE_TEST_ONLY"
assert data["object"] == "NewtonianEqualOppositeGravityForceActualValueTest"
assert "import Chronos.Frontier.NewtonianEqualOppositeGravityForceActualValueTest" in root

scaled = data["actual_values"]["earth_moon_scaled"]
assert scaled["massA"] == 6
assert scaled["massB"] == 2
assert scaled["distanceSquared"] == 3
assert scaled["gravitationalScale"] == 9
assert scaled["commonForceMagnitude"] == 36
assert scaled["forceOnAByB"] == -36
assert scaled["forceOnBByA"] == 36
assert scaled["forceSum"] == 0

unit = data["actual_values"]["balanced_unit"]
assert unit["massA"] == 4
assert unit["massB"] == 5
assert unit["distanceSquared"] == 2
assert unit["gravitationalScale"] == 3
assert unit["commonForceMagnitude"] == 30
assert unit["forceOnAByB"] == -30
assert unit["forceOnBByA"] == 30
assert unit["forceSum"] == 0

for token in required_lean_tokens:
    assert token in lean, token

for token in required_boundaries:
    assert token in data["does_not_prove"], token
    assert token in doc, token

print("NEWTONIAN_EQUAL_OPPOSITE_GRAVITY_FORCE_ACTUAL_VALUE_TEST_OK")
