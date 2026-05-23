#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/concrete_initial_data_class_specification_2026_05_23.json"
STATUS = ROOT / "docs/status/CONCRETE_INITIAL_DATA_CLASS_SPECIFICATION_2026_05_23.md"
LEAN = ROOT / "lean/Chronos/Frontier/ConcreteInitialDataClassSpecification.lean"

BLOCKED = [
    "SixFieldAnalyticPackageHypothesis",
    "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage",
    "Einstein-matter well-posedness",
    "non-symmetric persistence",
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
    "geometric regularity",
    "metric data",
    "second fundamental form data",
    "matter field data",
    "gauge condition",
    "boundary or asymptotic condition",
    "constraint equation class",
    "bootstrap energy functional",
    "nonsymmetric seed condition",
    "concentration seed condition",
    "six-field admissibility predicate",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    status = STATUS.read_text()
    lean = LEAN.read_text()

    assert data["artifact"] == "CONCRETE_INITIAL_DATA_CLASS_SPECIFICATION"
    assert data["status"] == "INITIAL_DATA_CLASS_SPECIFICATION_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["spacetime_dimension"] == 4
    assert data["spatial_dimension"] == 3
    assert data["next_admissible_object"] == "ConcreteMatterModelSpecification"

    for field in REQUIRED_FIELDS:
        assert field in data["required_fields"], field
        assert field in status, field

    for phrase in BLOCKED:
        assert phrase in data["blocked_use"], phrase
        assert phrase in status, phrase

    assert "provesSixFieldAnalyticPackageHypothesis := False" in lean
    assert "concrete_initial_data_class_specification_does_not_prove_six_field" in lean

    print("Concrete initial data class specification verification OK.")
    print("Status:", data["status"])
    print("Next admissible object:", data["next_admissible_object"])

if __name__ == "__main__":
    main()
