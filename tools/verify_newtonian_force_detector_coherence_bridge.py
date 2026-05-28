import json
from pathlib import Path

ART = Path("artifacts/chronos/newtonian_force_detector_coherence_bridge_2026_05_28.json")
DOC = Path("docs/status/NEWTONIAN_FORCE_DETECTOR_COHERENCE_BRIDGE_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/NewtonianForceDetectorCoherenceBridge.lean")
ROOT = Path("lean/Chronos.lean")

required_boundaries = [
    "new gravitational force law",
    "physical detector accuracy",
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
    "import Chronos.Frontier.NewtonianEqualOppositeGravityForceActualValueTest",
    "import Chronos.Frontier.PhysicalDetectorFieldExtractionMap",
    "def detectorFieldFromNewtonianSample",
    "def detectorCoherentWithNewtonianForce",
    "detector_field_from_newtonian_sample_gate",
    "newtonian_force_detector_coherence_bridge",
    "actual_earth_moon_scaled_detector_coherence_values",
    "actual_balanced_unit_detector_coherence_values",
    "extractedActiveMass",
    "equalAndOppositeForces",
]

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
root = ROOT.read_text()

assert data["status"] == "RESTRICTED_FINITE_DETECTOR_COHERENCE_BRIDGE_ONLY"
assert data["object"] == "NewtonianForceDetectorCoherenceBridge"
assert "import Chronos.Frontier.NewtonianForceDetectorCoherenceBridge" in root

scaled = data["actual_values"]["earth_moon_scaled"]
assert scaled["commonForceMagnitude"] == 36
assert scaled["detectorCount"] == 2
assert scaled["detectorFieldSamples"] == [36, 36]
assert scaled["extractedActiveMass"] == 72
assert scaled["forceOnAByB"] == -36
assert scaled["forceOnBByA"] == 36
assert scaled["forceCoherent"] is True

unit = data["actual_values"]["balanced_unit"]
assert unit["commonForceMagnitude"] == 30
assert unit["detectorCount"] == 2
assert unit["detectorFieldSamples"] == [30, 30]
assert unit["extractedActiveMass"] == 60
assert unit["forceOnAByB"] == -30
assert unit["forceOnBByA"] == 30
assert unit["forceCoherent"] is True

for token in required_lean_tokens:
    assert token in lean, token

for token in required_boundaries:
    assert token in data["does_not_prove"], token
    assert token in doc, token

print("NEWTONIAN_FORCE_DETECTOR_COHERENCE_BRIDGE_OK")
