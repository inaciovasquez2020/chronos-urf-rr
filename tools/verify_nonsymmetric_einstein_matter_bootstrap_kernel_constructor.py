#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean_file = ROOT / "lean/Chronos/Frontier/NonSymmetricEinsteinMatterBootstrapKernelConstructor.lean"
artifact_file = ROOT / "artifacts/chronos/nonsymmetric_einstein_matter_bootstrap_kernel_constructor_2026_05_22.json"
doc_file = ROOT / "docs/status/NONSYMMETRIC_EINSTEIN_MATTER_BOOTSTRAP_KERNEL_CONSTRUCTOR_2026_05_22.md"
chronos_file = ROOT / "lean/Chronos.lean"

lean = lean_file.read_text()
artifact = json.loads(artifact_file.read_text())
doc = doc_file.read_text()
chronos = chronos_file.read_text()

assert "import Chronos.Frontier.NonSymmetricEinsteinMatterBootstrapKernelConstructor" in chronos
assert "import Chronos.Frontier.GravityClosureKernelTarget" in lean
assert "theorem nonSymmetricEinsteinMatterBootstrapKernel_constructor" in lean
assert "theorem gravityClosureKernelTarget_from_supplied_fields" in lean
assert "theorem collapseGate_from_supplied_bootstrap_fields" in lean

assert artifact["status"] == "SUPPLIED_FIELD_CONSTRUCTOR_CLOSED_PDE_EXISTENCE_OPEN"
assert artifact["next_admissible_object"] == "GENUINE_EINSTEIN_MATTER_PDE_FIELD_SUPPLY_THEOREM"

for token in [
    "unrestricted gravity closure",
    "cosmic censorship",
    "hoop conjecture",
    "four-dimensional collapse theorem",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "Einstein-matter PDE existence",
    "Einstein-matter PDE regularity",
    "Einstein-matter PDE continuation",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in artifact["does_not_prove"]
    assert token in doc

print("Non-symmetric Einstein-matter bootstrap kernel constructor verification OK.")
print(f"Status: {artifact['status']}")
print(f"Next admissible object: {artifact['next_admissible_object']}")
