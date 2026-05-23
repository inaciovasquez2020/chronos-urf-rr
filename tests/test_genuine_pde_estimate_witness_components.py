import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_genuine_pde_components_artifact_status():
    data = json.loads(
        (ROOT / "artifacts/chronos/genuine_pde_estimate_witness_components_2026_05_22.json").read_text()
    )
    assert data["status"] == "FOUR_COMPONENT_ASSEMBLY_CLOSED_PDE_COMPONENT_PROOFS_OPEN"
    assert data["repository"] == "chronos-urf-rr"
    assert data["next_admissible_object"] == "GENUINE_PDE_ESTIMATE_WITNESS_COMPONENTS_EXIST"

def test_genuine_pde_components_four_component_names():
    data = json.loads(
        (ROOT / "artifacts/chronos/genuine_pde_estimate_witness_components_2026_05_22.json").read_text()
    )
    assert data["four_components"] == [
        "constraint_propagation",
        "energy_condition_preservation",
        "continuation_up_to_collapse_threshold",
        "collapse_criterion_from_restricted_seed",
    ]

def test_genuine_pde_components_lean_surface():
    lean = (ROOT / "lean/Chronos/Frontier/GenuinePDEEstimateWitnessComponents.lean").read_text()
    assert "structure GenuinePDEEstimateWitnessComponents" in lean
    assert "def genuinePDEEstimateWitness_from_components" in lean
    assert "theorem analyticEstimatePackageExists_from_genuinePDEComponents" in lean
    assert "theorem bootstrapKernel_from_genuinePDEComponents" in lean
    assert "theorem collapseGate_from_genuinePDEComponents" in lean
    assert "def GenuinePDEEstimateWitnessComponentsExist : Prop" in lean
    assert "axiom " not in lean

def test_genuine_pde_components_boundaries():
    data = json.loads(
        (ROOT / "artifacts/chronos/genuine_pde_estimate_witness_components_2026_05_22.json").read_text()
    )
    doc = (ROOT / "docs/status/GENUINE_PDE_ESTIMATE_WITNESS_COMPONENTS_2026_05_22.md").read_text()
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
        assert token in data["does_not_prove"]
        assert token in doc
