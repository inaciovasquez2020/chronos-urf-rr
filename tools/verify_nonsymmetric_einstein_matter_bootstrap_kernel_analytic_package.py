#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/nonsymmetric_einstein_matter_bootstrap_kernel_analytic_package_2026_05_22.json"
STATUS = ROOT / "docs/status/NONSYMMETRIC_EINSTEIN_MATTER_BOOTSTRAP_KERNEL_ANALYTIC_PACKAGE_2026_05_22.md"
LEAN = ROOT / "lean/Chronos/Frontier/NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage.lean"
ROOT_IMPORT = ROOT / "Chronos.lean"

REQUIRED_LEAN_TOKENS = [
    "structure NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage",
    "def analytic_package_to_constructor_input",
    "theorem analytic_package_implies_constructor_input",
    "theorem analytic_package_implies_existence_target",
    "theorem analytic_package_closes_conditional_gravity_package",
    "theorem analytic_package_no_overclaim_boundary",
]

REMAINING_OBJECTS = [
    "analyticPackage",
    "pdeWellPosedness",
    "nonsymmetricEvolutionPersistence",
    "admissibilityPreservation",
    "concentrationTransport",
    "finiteTimeCollapseAlternative",
]

BOUNDARY_TOKENS = [
    "analytic package",
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
    lean_text = LEAN.read_text()
    status_text = STATUS.read_text()
    import_text = ROOT_IMPORT.read_text()

    assert data["status"] == "ANALYTIC_PACKAGE_INPUT_ONLY_NOT_PROVED"
    assert data["object"] == "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage"
    assert "NonSymmetricEinsteinMatterBootstrapKernelConstructorInput" in data["sufficient_for"]
    assert "NonSymmetricEinsteinMatterBootstrapKernelExistenceTarget" in data["sufficient_for"]
    assert "import Chronos.Frontier.NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage" in import_text

    for token in REQUIRED_LEAN_TOKENS:
        assert token in lean_text, token

    for token in REMAINING_OBJECTS:
        assert token in data["remaining_missing_objects"], token
        assert token in status_text, token

    for token in BOUNDARY_TOKENS:
        assert token in data["does_not_prove"], token
        assert token in status_text, token

    words = lean_text.replace("/", " ").replace("-", " ").replace("!", " ").split()
    for forbidden in ["sorry", "admit", "axiom"]:
        assert forbidden not in words, forbidden

    print("Non-symmetric Einstein-matter bootstrap kernel analytic package verification OK.")
    print(f"Status: {data['status']}")
    print(f"Minimal missing assumption: {data['minimal_missing_assumption']}")

if __name__ == "__main__":
    main()
