#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/wellposed_nonsymmetric_collapse_data_2026_05_22.json"
STATUS = ROOT / "docs/status/WELLPPOSED_NONSYMMETRIC_COLLAPSE_DATA_2026_05_22.md"
LEAN = ROOT / "lean/Chronos/Frontier/WellPosedNonSymmetricCollapseData.lean"
ROOT_IMPORT = ROOT / "Chronos.lean"

TOKENS = [
    "structure WellPosedNonSymmetricCollapseData",
    "closure : NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage base",
    "theorem restricted_analytic_package",
    "theorem restricted_constructor_input",
    "theorem restricted_existence_target",
    "theorem restricted_package_no_overclaim_boundary",
]

BOUNDARY = [
    "SixFieldAnalyticPackageHypothesis",
    "unrestricted analytic package",
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

    assert data["status"] == "RESTRICTED_PACKAGE_THEOREM_ONLY"
    assert data["object"] == "WellPosedNonSymmetricCollapseData"
    assert "import Chronos.Frontier.WellPosedNonSymmetricCollapseData" in root

    for token in TOKENS:
        assert token in lean, token

    for item in BOUNDARY:
        assert item in data["does_not_prove"], item
        assert item in status, item

    words = lean.replace("/", " ").replace("-", " ").replace("!", " ").split()
    for forbidden in ["sorry", "admit", "axiom"]:
        assert forbidden not in words, forbidden

    print("Well-posed non-symmetric collapse data verification OK.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
