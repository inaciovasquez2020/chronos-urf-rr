import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_admissibility_gated_bridge_ingredient_kernel_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/admissibility_gated_bridge_ingredient_kernel_2026_05_24.json").read_text()
    )

    assert data["status"] == "ADMISSIBILITY_GATED_BRIDGE_INGREDIENT_KERNEL_ADDED_THEOREM_TARGETS_OPEN"
    assert data["new_bridge_ingredient"] == "AdmissibilityGatedBridgeIngredientKernel"
    assert data["ingredient_count"] == 3
    assert data["theorem_target_closure_count"] == 0
    assert len(data["ingredients"]) == 3
    assert len(data["gates"]) == 3
    assert len(data["closed_kernel_facts"]) == 6


def test_admissibility_gated_bridge_ingredient_kernel_lean_tokens():
    text = (ROOT / "lean/Chronos/Frontier/AdmissibilityGatedBridgeIngredientKernel.lean").read_text()

    for token in [
        "structure AdmissibilityGate",
        "structure BridgeIngredientKernel",
        "def R2AdmissibilityGatedBridgeIngredient",
        "def R3AdmissibilityGatedBridgeIngredient",
        "def NonFactorisationAdmissibilityGatedBridgeIngredient",
        "theorem r2_gate_excludes_refuted_naive_route_class",
        "theorem r3_gate_excludes_refuted_naive_route_class",
        "theorem non_factorisation_gate_excludes_refuted_naive_route_class",
        "theorem no_theorem_target_closed_by_admissibility_gated_kernel",
    ]:
        assert token in text


def test_admissibility_gated_bridge_ingredient_kernel_boundaries():
    text = (ROOT / "docs/status/ADMISSIBILITY_GATED_BRIDGE_INGREDIENT_KERNEL_2026_05_24.md").read_text()

    for token in [
        "ADMISSIBILITY_GATED_BRIDGE_INGREDIENT_KERNEL_ADDED_THEOREM_TARGETS_OPEN",
        "DiameterSeparationFillingObstructionProofTarget",
        "UniformLocalTypeCapacityProofTarget",
        "NonFactorisationBridgeProofTarget",
        "FourBridgesSourceSolved theorem closure",
        "R2 theorem target closure",
        "R3 theorem target closure",
        "NON_FACTORISATION theorem target closure",
        "Chronos-RR",
        "H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert token in text
