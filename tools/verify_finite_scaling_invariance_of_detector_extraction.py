import json
from pathlib import Path

ART = Path("artifacts/chronos/finite_scaling_invariance_of_detector_extraction_2026_05_28.json")
DOC = Path("docs/status/FINITE_SCALING_INVARIANCE_OF_DETECTOR_EXTRACTION_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/FiniteScalingInvarianceOfDetectorExtraction.lean")
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
    "import Chronos.Frontier.NewtonianForceDetectorCoherenceBridge",
    "def detectorExtractedActiveMassFromNewtonianSample",
    "detector_extracted_active_mass_eq_common_force_sum",
    "finite_scaling_invariance_of_detector_extraction",
    "actual_60_to_30_detector_scaling_values",
    "actual_72_to_36_detector_scaling_values",
    "actual_90_to_30_detector_scaling_values",
    "Nat.left_distrib",
]

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
root = ROOT.read_text()

assert data["status"] == "FINITE_SCALING_INVARIANCE_BRIDGE_ONLY"
assert data["object"] == "FiniteScalingInvarianceOfDetectorExtraction"
assert "import Chronos.Frontier.FiniteScalingInvarianceOfDetectorExtraction" in root

assert data["general_invariant"]["finite_style"] == "Nat only"

pairs = data["actual_values"]
assert pairs["scaling_60_to_30"]["k"] == 2
assert pairs["scaling_60_to_30"]["scaledExtractedActiveMass"] == 120
assert pairs["scaling_60_to_30"]["baseExtractedActiveMass"] == 60
assert pairs["scaling_60_to_30"]["scaledExtractedActiveMass"] == (
    pairs["scaling_60_to_30"]["k"] * pairs["scaling_60_to_30"]["baseExtractedActiveMass"]
)

assert pairs["scaling_72_to_36"]["k"] == 2
assert pairs["scaling_72_to_36"]["scaledExtractedActiveMass"] == 144
assert pairs["scaling_72_to_36"]["baseExtractedActiveMass"] == 72
assert pairs["scaling_72_to_36"]["scaledExtractedActiveMass"] == (
    pairs["scaling_72_to_36"]["k"] * pairs["scaling_72_to_36"]["baseExtractedActiveMass"]
)

assert pairs["scaling_90_to_30"]["k"] == 3
assert pairs["scaling_90_to_30"]["scaledExtractedActiveMass"] == 180
assert pairs["scaling_90_to_30"]["baseExtractedActiveMass"] == 60
assert pairs["scaling_90_to_30"]["scaledExtractedActiveMass"] == (
    pairs["scaling_90_to_30"]["k"] * pairs["scaling_90_to_30"]["baseExtractedActiveMass"]
)

for token in required_lean_tokens:
    assert token in lean, token

for token in required_boundaries:
    assert token in data["does_not_prove"], token
    assert token in doc, token

print("FINITE_SCALING_INVARIANCE_OF_DETECTOR_EXTRACTION_OK")
