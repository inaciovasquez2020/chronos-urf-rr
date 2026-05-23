#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean_file = ROOT / "lean/Chronos/Frontier/AnalyticEstimatePackageExistsProof.lean"
artifact_file = ROOT / "artifacts/chronos/analytic_estimate_package_exists_proof_2026_05_22.json"
doc_file = ROOT / "docs/status/ANALYTIC_ESTIMATE_PACKAGE_EXISTS_PROOF_2026_05_22.md"
chronos_file = ROOT / "lean/Chronos.lean"

lean = lean_file.read_text()
artifact = json.loads(artifact_file.read_text())
doc = doc_file.read_text()
chronos = chronos_file.read_text()

assert "import Chronos.Frontier.AnalyticEstimatePackageExistsProof" in chronos
assert "import Chronos.Frontier.GravityClosureKernelTarget" in lean
assert "structure ToolkitAdmissibleRegion" in lean
assert "structure AnalyticEstimatePackage" in lean
assert "def AnalyticEstimatePackageExists : Prop" in lean
assert "axiom AnalyticEstimatePackageExists" not in lean
assert "theorem analyticEstimatePackageExists_syntheticInterfaceProof" in lean
assert "theorem bootstrapKernel_from_analyticEstimatePackageExists" in lean
assert "theorem bootstrapKernel_from_syntheticAnalyticEstimatePackage" in lean
assert "theorem collapseGate_from_analyticEstimatePackageExists" in lean
assert "theorem collapseGate_from_syntheticAnalyticEstimatePackage" in lean

assert artifact["status"] == "SYNTHETIC_INTERFACE_PROOF_CLOSED_GENUINE_PDE_PROOF_OPEN"
assert artifact["proved_object"] == "AnalyticEstimatePackageExists inside the abstract Prop-valued interface"
assert artifact["next_admissible_object"] == "GENUINE_ANALYTIC_ESTIMATE_PACKAGE_EXISTS_PROOF"

for token in [
    "genuine Einstein-matter PDE existence",
    "genuine Einstein-matter PDE regularity",
    "genuine Einstein-matter PDE continuation",
    "unconditional gravity closure",
    "unrestricted gravity closure",
    "cosmic censorship",
    "hoop conjecture",
    "four-dimensional collapse theorem",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in artifact["does_not_prove"]
    assert token in doc

print("Analytic estimate package exists proof verification OK.")
print(f"Status: {artifact['status']}")
print(f"Next admissible object: {artifact['next_admissible_object']}")
