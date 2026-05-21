#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/nonsymmetric_einstein_matter_bootstrap_kernel_existence_frontier_2026_05_21.json"
STATUS = ROOT / "docs/status/NONSYMMETRIC_EINSTEIN_MATTER_BOOTSTRAP_KERNEL_EXISTENCE_FRONTIER_2026_05_21.md"
LEAN = ROOT / "lean/Chronos/Frontier/NonSymmetricEinsteinMatterBootstrapKernelExistenceFrontier.lean"
ROOT_IMPORT = ROOT / "Chronos.lean"

REQUIRED_LEAN_TOKENS = [
    "structure GenuineNonSymmetricEinsteinMatterPDEData",
    "def NonSymmetricEinsteinMatterBootstrapKernelExistenceTarget",
    "theorem existence_target_unpacks",
    "theorem supplied_kernel_closes_conditional_gravity_package",
    "theorem existence_target_closes_conditional_gravity_package",
    "theorem existence_frontier_no_overclaim_boundary",
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
    assert data["status"] == "FRONTIER_OPEN_TARGET_ONLY"
    assert data["target"] == "NonSymmetricEinsteinMatterBootstrapKernelExistenceTarget"

    lean_text = LEAN.read_text()
    status_text = STATUS.read_text()
    import_text = ROOT_IMPORT.read_text()

    assert "import Chronos.Frontier.NonSymmetricEinsteinMatterBootstrapKernelExistenceFrontier" in import_text

    for token in REQUIRED_LEAN_TOKENS:
        assert token in lean_text, token

    for token in BOUNDARY_TOKENS:
        assert token in status_text, token
        assert token in data["does_not_prove"], token

    words = lean_text.replace("/", " ").replace("-", " ").replace("!", " ").split()
    for token in ["sorry", "admit", "axiom"]:
        assert token not in words, token

    print("Non-symmetric bootstrap-kernel existence frontier verification OK.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
