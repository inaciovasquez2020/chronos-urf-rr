from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "lean/Chronos/Frontier/GravityNonSymmetricEinsteinMatterCollapseCompactness.lean",
    ROOT / "lean/Chronos/Frontier/ActiveGravityCarrierBinding.lean",
    ROOT / "lean/Chronos/Frontier/RestrictedSphericalCollapseEntropyGap.lean",
    ROOT / "lean/Chronos/Frontier/NonSphericalStabilityTransfer.lean",
    ROOT / "docs/status/GRAVITY_NONSYMMETRIC_COLLAPSE_COMPACTNESS_BOUNDARY_2026_05_17.md",
    ROOT / "artifacts/chronos/gravity_nonsymmetric_collapse_compactness_boundary_2026_05_17.json",
]

REQUIRED = [
    "NonSymmetricEinsteinMatterCollapseCompactness",
    "FRONTIER_OPEN",
    "ActiveGravityCarrierBinding",
    "ACTIVE_BINDING_INTERFACE_ONLY",
    "RestrictedSphericalCollapseEntropyGap",
    "NonSphericalStabilityTransfer",
    "conditional",
    "Cosmic Censorship",
    "the Hoop Conjecture",
    "unconditional QL_CollapseGate",
    "unconditional UniversalBoundaryCompactness",
]

FORBIDDEN = [
    "proves Cosmic Censorship",
    "solves Cosmic Censorship",
    "proves the Hoop Conjecture",
    "solves the Hoop Conjecture",
    "proves Hoop Conjecture",
    "solves Hoop Conjecture",
    "unconditional QL_CollapseGate is closed",
    "unconditional UniversalBoundaryCompactness is closed",
    "proves unrestricted Chronos-RR",
    "proves H4.1/FGL",
    "proves P vs NP",
    "solves P vs NP",
    "solves a Clay problem",
]

def main() -> None:
    missing_files = [str(p.relative_to(ROOT)) for p in FILES if not p.exists()]
    assert not missing_files, f"Missing files: {missing_files}"

    combined = "\n".join(p.read_text() for p in FILES)
    lowered = combined.lower()

    for token in REQUIRED:
        assert token.lower() in lowered, token

    for token in FORBIDDEN:
        assert token.lower() not in lowered, token

    chronos = (ROOT / "lean/Chronos.lean").read_text()
    imports = [
        "import Chronos.Frontier.GravityNonSymmetricEinsteinMatterCollapseCompactness",
        "import Chronos.Frontier.ActiveGravityCarrierBinding",
        "import Chronos.Frontier.RestrictedSphericalCollapseEntropyGap",
        "import Chronos.Frontier.NonSphericalStabilityTransfer",
    ]
    for imp in imports:
        assert imp in chronos, imp

    print("Gravity nonsymmetric collapse compactness boundary verified.")

if __name__ == "__main__":
    main()
