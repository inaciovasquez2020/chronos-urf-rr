#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/nonsymmetric_gravity_open_problem_minimal_blocker_2026_05_22.json"
STATUS = ROOT / "docs/status/NONSYMMETRIC_GRAVITY_OPEN_PROBLEM_MINIMAL_BLOCKER_2026_05_22.md"
LEAN = ROOT / "lean/Chronos/Frontier/NonSymmetricGravityOpenProblemMinimalBlocker.lean"
ROOT_IMPORT = ROOT / "Chronos.lean"

FIELDS = [
    "pdeEvolution",
    "nonsymmetricEvolution",
    "initialAdmissible",
    "surfaceRealization",
    "concentrationTransport",
    "finiteTimeCollapseAlternative",
]

BOUNDARY = [
    "analytic package",
    "any single field implies the other five fields",
    "pdeEvolution from PDE well-posedness",
    "nonsymmetric evolution persistence",
    "admissibility preservation",
    "concentration transport",
    "finite-time collapse alternative",
    "unrestricted cosmic censorship",
    "unrestricted hoop theorem",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "P vs NP",
    "any Clay problem",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    status = STATUS.read_text()
    lean = LEAN.read_text()
    root = ROOT_IMPORT.read_text()

    assert data["status"] == "OPEN_PROBLEM_FRONTIER_C_MINIMAL_BLOCKER"
    assert data["weakest_sufficient_object"] == "SixFieldAnalyticPackageHypothesis"
    assert data["corrected_false_claim"] == "A single uniform field does not close the six-field analytic package."
    assert "import Chronos.Frontier.NonSymmetricGravityOpenProblemMinimalBlocker" in root

    for token in [
        "def openProblem : Prop",
        "structure SixFieldAnalyticPackageHypothesis",
        "theorem six_field_hypothesis_closes_open_problem",
        "theorem open_problem_minimal_blocker_no_overclaim_boundary",
    ]:
        assert token in lean, token

    for field in FIELDS:
        assert field in data["required_fields"]
        assert field in data["single_fields_not_sufficient_alone"]
        assert field in status

    for item in BOUNDARY:
        assert item in data["does_not_prove"]
        assert item in status

    words = lean.replace("/", " ").replace("-", " ").replace("!", " ").split()
    for forbidden in ["sorry", "admit", "axiom"]:
        assert forbidden not in words, forbidden

    print("Non-symmetric gravity open problem minimal blocker verification OK.")
    print(f"Status: {data['status']}")
    print(f"Weakest sufficient object: {data['weakest_sufficient_object']}")

if __name__ == "__main__":
    main()
