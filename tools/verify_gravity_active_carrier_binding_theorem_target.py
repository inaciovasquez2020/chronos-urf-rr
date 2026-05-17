from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "lean/Chronos/Frontier/GravityActiveCarrierBindingTheoremTarget.lean",
    ROOT / "docs/status/GRAVITY_ACTIVE_CARRIER_BINDING_THEOREM_TARGET_2026_05_17.md",
    ROOT / "artifacts/chronos/gravity_active_carrier_binding_theorem_target_2026_05_17.json",
]

REQUIRED = [
    "GravityActiveCarrierBindingTheoremTarget",
    "EinsteinMatterEvolutionActsOnCarrier",
    "GravityCarrierEntropyMass",
    "CertificateSurfaceFactorsThroughActiveCarrier",
    "certificateSurfaceFactorsThroughActiveCarrier_conditional",
    "CONDITIONAL",
    "ACTIVE_BINDING_THEOREM_TARGET_ONLY",
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
    "gravity theorem-level closure",
    "Cosmic Censorship is solved",
    "Hoop Conjecture is solved",
]

def main() -> None:
    missing = [str(p.relative_to(ROOT)) for p in FILES if not p.exists()]
    assert not missing, f"Missing files: {missing}"

    combined = "\n".join(p.read_text() for p in FILES)
    lowered = combined.lower()

    for token in REQUIRED:
        assert token.lower() in lowered, token

    for token in FORBIDDEN:
        assert token.lower() not in lowered, token

    chronos = (ROOT / "lean/Chronos.lean").read_text()
    assert (
        "import Chronos.Frontier.GravityActiveCarrierBindingTheoremTarget" in chronos
    ), "missing Chronos.lean import"

    print("Gravity active carrier binding theorem target verified.")

if __name__ == "__main__":
    main()
