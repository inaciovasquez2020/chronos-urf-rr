from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/GravityBoundaryCompactnessCollapseGate.lean").read_text()
status = Path("docs/status/GRAVITY_BOUNDARY_COMPACTNESS_COLLAPSE_GATE_2026_05_16.md").read_text()
artifact = json.loads(Path("artifacts/chronos/gravity_boundary_compactness_collapse_gate_2026_05_16.json").read_text())

required_lean = [
    "structure PhysicallyAdmissibleRegion",
    "structure BoundaryAccessibleObservable",
    "structure GravityBoundaryFiniteDetectorAlgebra",
    "structure CovariantEntropyBound",
    "def UniversalBoundaryCompactness",
    "def QL_CollapseGate",
    "theorem finite_detector_algebra_implies_universal_boundary_compactness",
    "theorem covariant_entropy_bound_implies_universal_boundary_compactness",
    "theorem universal_boundary_compactness_implies_QL_CollapseGate",
    "theorem finite_detector_algebra_implies_QL_CollapseGate",
    "theorem covariant_entropy_bound_implies_QL_CollapseGate",
]

required_status = [
    "CONDITIONAL_BOUNDARY_COMPACTNESS_ROUTE_ONLY",
    "Conditional surface only.",
    "Does not prove:",
    "unconditional Universal Boundary Compactness",
    "unconditional QL_CollapseGate",
    "Cosmic Censorship",
    "the Hoop Conjecture",
    "any Clay problem",
]

for phrase in required_lean:
    assert phrase in lean, phrase

for phrase in required_status:
    assert phrase in status, phrase

assert artifact["status"] == "CONDITIONAL_BOUNDARY_COMPACTNESS_ROUTE_ONLY"

for phrase in required_lean[:6]:
    assert phrase.split()[-1] in artifact["formal_objects"] or phrase.split()[-1].replace("GravityBoundaryFiniteDetectorAlgebra", "FiniteDetectorAlgebra") in artifact["formal_objects"], phrase

forbidden = [
    "proves Einstein dynamics",
    "proves finite-energy matter admissibility",
    "proves backreaction control",
    "proves diffeomorphism-invariant gravitational observables",
    "proves finite detector algebra",
    "proves covariant entropy bound",
    "proves unconditional Universal Boundary Compactness",
    "proves unconditional QL_CollapseGate",
    "proves unrestricted nonspherical collapse exclusion",
    "proves Cosmic Censorship",
    "proves the Hoop Conjecture",
    "solves Cosmic Censorship",
    "solves the Hoop Conjecture",
    "solves a Clay problem",
]

combined = (lean + "\n" + status + "\n" + json.dumps(artifact)).lower()
for token in forbidden:
    assert token.lower() not in combined, token

print("Gravity boundary compactness collapse gate verified.")
