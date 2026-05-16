#!/usr/bin/env python3
from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/GravityA3BoundaryCompactnessFromFiniteDetector.lean")
status = Path("docs/status/GRAVITY_A3_BOUNDARY_COMPACTNESS_FROM_FINITE_DETECTOR_2026_05_16.md")
artifact = Path("artifacts/chronos/gravity_a3_boundary_compactness_from_finite_detector_2026_05_16.json")
root = Path("lean/Chronos.lean")

for p in [lean, status, artifact, root]:
    assert p.exists(), f"missing {p}"

lean_text = lean.read_text()
status_text = status.read_text()
artifact_data = json.loads(artifact.read_text())
root_text = root.read_text()

required_lean = [
    "namespace GravityA3BoundaryCompactnessFromFiniteDetector",
    "class BoundaryTopologicalSpace",
    "class BoundaryCompactSpace",
    "class FiniteDetectorAlgebra",
    "class SpectralCutoff",
    "class FiniteEnergyMatterAdmissible",
    "class BackreactionControlled",
    "class BoundaryCompactness",
    "class PhysicalToTopologicalCompactnessInput",
    "theorem BoundaryCompactness_of_compact_space",
    "theorem A3BoundaryCompactnessBridge",
    "structure A3BoundaryCompactnessStatusLock",
    "theorem a3_boundary_compactness_status_lock",
]

for phrase in required_lean:
    assert phrase in lean_text, phrase

assert artifact_data["status"] == "RESTRICTED_A3_DERIVATION_TARGET"
assert artifact_data["main_theorem"] == "A3BoundaryCompactnessBridge"
assert artifact_data["compactness_input"] == "PhysicalToTopologicalCompactnessInput"

required_status = [
    "Status: `RESTRICTED_A3_DERIVATION_TARGET`",
    "Conditional restricted A3 bridge only.",
    "Does not prove:",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted QL_CollapseGate",
    "Cosmic Censorship",
    "the Hoop Conjecture",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status_text, phrase

assert "import Chronos.Frontier.GravityA3BoundaryCompactnessFromFiniteDetector" in root_text

forbidden_positive_claims = [
    "proves unrestricted UniversalBoundaryCompactness",
    "proves unrestricted QL_CollapseGate",
    "proves Cosmic Censorship",
    "proves the Hoop Conjecture",
    "proves unrestricted Chronos-RR",
    "proves H4.1/FGL",
    "proves P vs NP",
    "solves P vs NP",
    "solves any Clay problem",
]

combined = "\n".join([lean_text, status_text, json.dumps(artifact_data)])
for token in forbidden_positive_claims:
    assert token.lower() not in combined.lower(), token

print("Gravity A3 boundary compactness bridge verified: RESTRICTED_A3_DERIVATION_TARGET.")
