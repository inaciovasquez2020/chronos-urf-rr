import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_four_component_reduction_artifact_status():
    data = json.loads(
        (ROOT / "artifacts/chronos/genuine_four_pde_component_existence_reduction_2026_05_22.json").read_text()
    )
    assert data["status"] == "FOUR_COMPONENT_EXISTENCE_REDUCTION_CLOSED_COMPONENT_PROOFS_OPEN"
    assert data["next_admissible_object"] == "GENUINE_FOUR_PDE_COMPONENT_EXISTENCE_REDUCTION_TARGET"

def test_four_component_reduction_lean_surface():
    lean = (ROOT / "lean/Chronos/Frontier/GenuineFourPDEComponentExistenceReduction.lean").read_text()
    assert "structure GenuineConstraintPropagationComponent" in lean
    assert "structure GenuineEnergyConditionPreservationComponent" in lean
    assert "structure GenuineContinuationUpToCollapseThresholdComponent" in lean
    assert "structure GenuineCollapseCriterionFromRestrictedSeedComponent" in lean
    assert "def genuinePDEEstimateWitnessComponents_from_four_components" in lean
    assert "theorem genuinePDEEstimateWitnessComponentsExist_from_four_component_target" in lean
    assert "axiom " not in lean

def test_four_component_reduction_boundaries():
    data = json.loads(
        (ROOT / "artifacts/chronos/genuine_four_pde_component_existence_reduction_2026_05_22.json").read_text()
    )
    doc = (ROOT / "docs/status/GENUINE_FOUR_PDE_COMPONENT_EXISTENCE_REDUCTION_2026_05_22.md").read_text()
    for token in [
        "constraint propagation PDE theorem",
        "energy-condition preservation PDE theorem",
        "continuation PDE theorem",
        "collapse criterion PDE theorem",
        "genuine Einstein-matter PDE existence",
        "genuine Einstein-matter PDE regularity",
        "genuine Einstein-matter PDE continuation",
        "unconditional gravity closure",
        "unrestricted gravity closure",
        "cosmic censorship",
        "hoop conjecture",
        "four-dimensional collapse theorem",
        "Chronos-RR",
        "H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert token in data["does_not_prove"]
        assert token in doc
