#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/nonsymmetric_einstein_matter_bootstrap_kernel_2026_05_21.json"
STATUS = ROOT / "docs/status/NONSYMMETRIC_EINSTEIN_MATTER_BOOTSTRAP_KERNEL_2026_05_21.md"
LEAN = ROOT / "lean/Chronos/Frontier/NonSymmetricEinsteinMatterBootstrapKernel.lean"
ROOT_IMPORT = ROOT / "Chronos.lean"

REQUIRED_LEAN_TOKENS = [
    "structure NonSymmetricEinsteinMatterBootstrapKernel",
    "theorem bootstrap_kernel_derives_finite_time_pde_outcome",
    "theorem bootstrap_kernel_closes_restricted_gravity",
    "theorem bootstrap_kernel_final_conditional_gravity_package",
    "theorem final_gravity_no_overclaim_boundary",
    "DoesNotProve_unrestrictedCosmicCensorship",
    "DoesNotProve_unrestrictedHoopTheorem",
    "DoesNotProve_ClayClosure",
]

BOUNDARY_TOKENS = [
    "unrestricted cosmic censorship",
    "unrestricted hoop theorem",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "P vs NP",
    "any Clay problem",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "CONDITIONAL_KERNEL_CLOSED"
    assert data["weakest_missing_object"] == (
        "Existence of NonSymmetricEinsteinMatterBootstrapKernel "
        "for genuine non-symmetric Einstein-matter PDE data"
    )

    lean_text = LEAN.read_text()
    status_text = STATUS.read_text()
    import_text = ROOT_IMPORT.read_text()

    assert "import Chronos.Frontier.NonSymmetricEinsteinMatterBootstrapKernel" in import_text

    for token in REQUIRED_LEAN_TOKENS:
        assert token in lean_text, token

    for token in BOUNDARY_TOKENS:
        assert token in status_text, token
        assert token in data["does_not_prove"], token

    forbidden_exact = ["sorry", "admit", "axiom"]
    words = lean_text.replace("/", " ").replace("-", " ").replace("!", " ").split()
    for token in forbidden_exact:
        assert token not in words, token

    print("Non-symmetric Einstein-matter bootstrap kernel verification OK.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
