#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/nonsymmetric_einstein_matter_bootstrap_kernel_constructor_input_2026_05_22.json"
STATUS = ROOT / "docs/status/NONSYMMETRIC_EINSTEIN_MATTER_BOOTSTRAP_KERNEL_CONSTRUCTOR_INPUT_2026_05_22.md"
LEAN = ROOT / "lean/Chronos/Frontier/NonSymmetricEinsteinMatterBootstrapKernelConstructorInput.lean"
ROOT_IMPORT = ROOT / "Chronos.lean"

REQUIRED_LEAN_TOKENS = [
    "structure NonSymmetricEinsteinMatterBootstrapKernelConstructorInput",
    "def kernel_from_constructor_input",
    "theorem constructor_input_implies_existence_target",
    "theorem constructor_input_closes_conditional_gravity_package",
    "theorem constructor_input_no_overclaim_boundary",
    "pdeEvolution",
    "nonsymmetricEvolution",
    "initialAdmissible",
    "surfaceRealization",
    "concentrationTransport",
    "finiteTimeCollapseAlternative",
]

BOUNDARY_TOKENS = [
    "unrestricted cosmic censorship",
    "unrestricted hoop theorem",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "P vs NP",
    "any Clay problem",
]

REMAINING_OBJECTS = [
    "pdeEvolution",
    "nonsymmetricEvolution",
    "initialAdmissible",
    "surfaceRealization",
    "concentrationTransport",
    "finiteTimeCollapseAlternative",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    lean_text = LEAN.read_text()
    status_text = STATUS.read_text()
    import_text = ROOT_IMPORT.read_text()

    assert data["status"] == "CONSTRUCTOR_INPUT_ONLY_TARGET_REDUCED_NOT_SOLVED"
    assert data["object"] == "NonSymmetricEinsteinMatterBootstrapKernelConstructorInput"
    assert data["reduces_target"] == "NonSymmetricEinsteinMatterBootstrapKernelExistenceTarget"

    assert "import Chronos.Frontier.NonSymmetricEinsteinMatterBootstrapKernelConstructorInput" in import_text

    for token in REQUIRED_LEAN_TOKENS:
        assert token in lean_text, token

    for token in BOUNDARY_TOKENS:
        assert token in status_text, token
        assert token in data["does_not_prove"], token

    for token in REMAINING_OBJECTS:
        assert token in data["remaining_missing_objects"], token
        assert token in status_text, token

    words = lean_text.replace("/", " ").replace("-", " ").replace("!", " ").split()
    for token in ["sorry", "admit", "axiom"]:
        assert token not in words, token

    print("Non-symmetric Einstein-matter bootstrap kernel constructor input verification OK.")
    print(f"Status: {data['status']}")
    print(f"Remaining objects: {', '.join(data['remaining_missing_objects'])}")

if __name__ == "__main__":
    main()
