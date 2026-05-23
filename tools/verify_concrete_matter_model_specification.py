#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/concrete_matter_model_specification_2026_05_23.json"
STATUS = ROOT / "docs/status/CONCRETE_MATTER_MODEL_SPECIFICATION_2026_05_23.md"
LEAN = ROOT / "lean/Chronos/Frontier/ConcreteMatterModelSpecification.lean"

BLOCKED = [
    "SixFieldAnalyticPackageHypothesis",
    "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage",
    "Einstein-matter well-posedness",
    "non-symmetric persistence",
    "matter-coupling control",
    "concentration transport",
    "collapse-gate trigger",
    "cosmic censorship",
    "hoop conjecture",
    "gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

REQUIRED_FIELDS = [
    "matter field type",
    "matter equation",
    "Einstein-matter coupling",
    "stress-energy tensor definition",
    "stress-energy conservation law",
    "energy condition",
    "matter regularity class",
    "source-term control",
    "matter energy functional",
    "compatibility with ConcreteInitialDataClassSpecification",
    "compatibility with SixFieldAnalyticPackageInputSurface",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    status = STATUS.read_text()
    lean = LEAN.read_text()

    assert data["artifact"] == "CONCRETE_MATTER_MODEL_SPECIFICATION"
    assert data["status"] == "MATTER_MODEL_SPECIFICATION_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["spacetime_dimension"] == 4
    assert data["spatial_dimension"] == 3
    assert data["next_admissible_object"] == "BootstrapSlabToSixFieldSlotConstraintClosure"

    for field in REQUIRED_FIELDS:
        assert field in data["required_fields"], field
        assert field in status, field

    for phrase in BLOCKED:
        assert phrase in data["blocked_use"], phrase
        assert phrase in status, phrase

    assert "provesSixFieldAnalyticPackageHypothesis := False" in lean
    assert "concrete_matter_model_specification_does_not_prove_six_field" in lean

    print("Concrete matter model specification verification OK.")
    print("Status:", data["status"])
    print("Next admissible object:", data["next_admissible_object"])

if __name__ == "__main__":
    main()
