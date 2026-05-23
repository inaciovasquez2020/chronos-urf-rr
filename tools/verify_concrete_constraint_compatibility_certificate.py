#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/concrete_constraint_compatibility_certificate_2026_05_23.json"
doc = ROOT / "docs/status/CONCRETE_CONSTRAINT_COMPATIBILITY_CERTIFICATE_2026_05_23.md"
lean = ROOT / "lean/Chronos/Frontier/ConcreteConstraintCompatibilityCertificate.lean"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
assert data["id"] == "CONCRETE_CONSTRAINT_COMPATIBILITY_CERTIFICATE"
assert data["status"] == "CONCRETE_CONSTRAINT_COMPATIBILITY_CERTIFICATE_ONLY_NO_ANALYTIC_ESTIMATE_PROOF"
assert data["previous_frontier"] == "FILLED_CONCRETE_INITIAL_DATA_CLASS_ONLY_NO_ANALYTIC_ESTIMATE_PROOF"
assert data["object_type"] == "constructor_constraint_certificate"
assert data["input_object"] == "FILLED_CONCRETE_INITIAL_DATA_CLASS"

certified_gates = data["certified_gates"]
required_gates = [
    "hamiltonian_constraint_compatible",
    "momentum_constraint_compatible",
    "gauge_constraint_compatible",
    "matter_constraint_compatible",
    "boundary_constraint_compatible",
]
for gate in required_gates:
    assert certified_gates[gate] is True

required_boundaries = [
    "analytic estimate proof",
    "SixFieldAnalyticPackageHypothesis proof",
    "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage proof",
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
doc_text = doc.read_text()
for token in required_boundaries:
    assert token in data["does_not_prove"]
    assert token in doc_text

lean_text = lean.read_text()
assert "structure ConcreteConstraintCompatibilityCertificate" in lean_text
assert "canonicalConcreteConstraintCompatibilityCertificate_isCertified" in lean_text
assert "concreteConstraintCompatibilityCertificate_boundary_noAnalyticEstimateProof" in lean_text
assert "import Chronos.Frontier.ConcreteConstraintCompatibilityCertificate" in root_import.read_text()

print("Concrete constraint compatibility certificate verification OK.")
print("Status:", data["status"])
print("Next admissible object:", data["next_admissible_object"])
