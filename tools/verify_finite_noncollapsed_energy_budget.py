from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FiniteNonCollapsedEnergyBudget.lean")
artifact = Path("artifacts/chronos/finite_noncollapsed_energy_budget_2026_05_15.json")
status = Path("docs/status/CHRONOS_FINITE_NONCOLLAPSED_ENERGY_BUDGET_2026_05_15.md")

assert lean.exists(), lean
assert artifact.exists(), artifact
assert status.exists(), status

lean_text = lean.read_text()
artifact_text = artifact.read_text()
artifact_json = json.loads(artifact_text)
status_text = status.read_text()

required_lean = [
    "structure FiniteNonCollapsedEnergyBudgetInput",
    "finiteNonCollapsedEnergyBudget",
    "structure BoundarySpectralInput",
    "finiteSpectralCountingWitness",
    "structure BoundaryModeEnergyInput",
    "energyAccounting",
    "normalizedResolvedModeEnergyGrowth",
    "structure FiniteResolutionBinInput",
    "finiteResolutionBins",
    "def OperationalDetectorAlgebraFinite",
    "def UniversalBoundaryCompactnessConditional",
    "theorem compactness_from_finite_noncollapsed_energy_budget",
    "Nat.le_trans h_growth",
    "structure SphericalMisnerSharpClosureInput",
    "def spherical_misner_sharp_induces_finite_budget",
    "structure NonsphericalFiniteEnergyClosureInput",
    "def nonspherical_finite_energy_induces_budget",
    "structure QLCollapseGateOpenFrontier",
    "def UnrestrictedUniversalBoundaryCompactnessStatus",
    "CONDITIONAL_ON_FINITE_NONCOLLAPSED_ENERGY_BUDGET",
]

for token in required_lean:
    assert token in lean_text, token

assert artifact_json["status"] == "CONDITIONAL_ON_FINITE_NONCOLLAPSED_ENERGY_BUDGET"
assert artifact_json["core_theorem"] == "compactness_from_finite_noncollapsed_energy_budget"
assert artifact_json["formal_target"] == "UniversalBoundaryCompactnessConditional"
assert artifact_json["weakest_admissibility_axiom"] == "FiniteNonCollapsedEnergyBudget"

for token in [
    "unconditional unrestricted UniversalBoundaryCompactness",
    "QL_CollapseGate",
    "unrestricted nonspherical collapse exclusion",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay-problem closure",
]:
    assert token in artifact_json["not_proved"], token

required_status = [
    "Status: CONDITIONAL_ON_FINITE_NONCOLLAPSED_ENERGY_BUDGET",
    "compactness_from_finite_noncollapsed_energy_budget",
    "UniversalBoundaryCompactnessConditional",
    "FiniteNonCollapsedEnergyBudget",
    "SphericalMisnerSharpClosure",
    "NonsphericalFiniteEnergyClosure",
    "QL_CollapseGate",
    "This file does not prove:",
    "unconditional unrestricted UniversalBoundaryCompactness",
    "unrestricted nonspherical collapse exclusion",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "Unrestricted UniversalBoundaryCompactness remains conditional on FiniteNonCollapsedEnergyBudget.",
]

for token in required_status:
    assert token in status_text, token

forbidden = [
    "proves unconditional unrestricted UniversalBoundaryCompactness",
    "proves QL_CollapseGate",
    "proves unrestricted nonspherical collapse exclusion",
    "proves Cosmic Censorship",
    "proves the Hoop Conjecture",
    "proves unrestricted Chronos-RR",
    "proves H4.1/FGL",
    "proves P vs NP",
    "solves P vs NP",
    "solves a Clay problem",
    "unconditional UniversalBoundaryCompactness is closed",
]

combined = "\n".join([lean_text, artifact_text, status_text]).lower()
for token in forbidden:
    assert token.lower() not in combined, token

print("FiniteNonCollapsedEnergyBudget conditional compactness surface verified.")
