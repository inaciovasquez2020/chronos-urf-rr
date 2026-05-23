#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean_file = ROOT / "lean/Chronos/Frontier/AnalyticEstimatePackageExistsAxiom.lean"
artifact_file = ROOT / "artifacts/chronos/analytic_estimate_package_exists_axiom_2026_05_22.json"
doc_file = ROOT / "docs/status/ANALYTIC_ESTIMATE_PACKAGE_EXISTS_AXIOM_2026_05_22.md"
chronos_file = ROOT / "lean/Chronos.lean"

lean = lean_file.read_text()
artifact = json.loads(artifact_file.read_text())
doc = doc_file.read_text()
chronos = chronos_file.read_text()

assert "import Chronos.Frontier.AnalyticEstimatePackageExistsAxiom" in chronos
assert "import Chronos.Frontier.GravityClosureKernelTarget" in lean
assert "structure ToolkitAdmissibleRegion" in lean
assert "structure AnalyticEstimatePackage" in lean
assert "def AnalyticEstimatePackageExists : Prop" in lean
assert "axiom AnalyticEstimatePackageExists" not in lean
assert "theorem bootstrapKernel_from_analyticEstimatePackageExists" in lean
assert "theorem collapseGate_from_analyticEstimatePackageExists" in lean

assert artifact["status"] == "CONDITIONAL_ANALYTIC_PACKAGE_EXISTENCE_REDUCTION_ONLY_NO_UNCONDITIONAL_GRAVITY_PROOF"
assert artifact["proposition"] == "AnalyticEstimatePackageExists"
assert artifact["next_admissible_object"] == "ANALYTIC_ESTIMATE_PACKAGE_EXISTS_PROOF"

for token in [
    "unconditional gravity closure",
    "unrestricted gravity closure",
    "cosmic censorship",
    "hoop conjecture",
    "four-dimensional collapse theorem",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "unaxiomatized Einstein-matter PDE existence",
    "unaxiomatized Einstein-matter PDE regularity",
    "unaxiomatized Einstein-matter PDE continuation",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in artifact["does_not_prove"]
    assert token in doc

print("Analytic estimate package axiom verification OK.")
print(f"Status: {artifact['status']}")
print(f"Proposition: {artifact['proposition']}")
print(f"Next admissible object: {artifact['next_admissible_object']}")
