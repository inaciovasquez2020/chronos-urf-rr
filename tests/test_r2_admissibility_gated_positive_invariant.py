import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_r2_admissibility_gated_positive_invariant_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/r2_admissibility_gated_positive_invariant_2026_05_24.json").read_text()
    )

    assert data["status"] == "R2_POSITIVE_INVARIANT_INGREDIENT_CLOSED_THEOREM_TARGET_OPEN"
    assert data["lane"] == "R2"
    assert data["closed_ingredient"] == "R2ConcreteDiameterFillingCompatibilityInvariant"
    assert data["positive_invariant_ingredient_closed_count"] == 1
    assert data["r2_theorem_target_closure_count"] == 0
    assert len(data["closed_theorems"]) == 5


def test_r2_admissibility_gated_positive_invariant_lean_tokens():
    text = (ROOT / "lean/Chronos/Frontier/R2AdmissibilityGatedPositiveInvariant.lean").read_text()

    for token in [
        "structure R2DiameterFillingCompatibilityInvariant",
        "def R2ConcreteDiameterFillingCompatibilityInvariant",
        "def R2AdmissibilityGatedPositiveInvariantReady",
        "theorem r2_concrete_positive_invariant_ready",
        "theorem r2_concrete_positive_invariant_excludes_refuted_naive_class",
        "theorem r2_concrete_positive_invariant_supplies_diameter_stability",
        "theorem r2_concrete_positive_invariant_supplies_filling_compatibility",
        "theorem r2_concrete_positive_invariant_preserves_obstruction_witness",
        "theorem no_r2_theorem_target_closed_by_positive_invariant",
    ]:
        assert token in text


def test_r2_admissibility_gated_positive_invariant_boundaries():
    text = (ROOT / "docs/status/R2_ADMISSIBILITY_GATED_POSITIVE_INVARIANT_2026_05_24.md").read_text()

    for token in [
        "R2_POSITIVE_INVARIANT_INGREDIENT_CLOSED_THEOREM_TARGET_OPEN",
        "DiameterSeparationFillingObstructionProofTarget",
        "R2 theorem target closure",
        "R3 theorem target closure",
        "NON_FACTORISATION theorem target closure",
        "FourBridgesSourceSolved theorem closure",
        "Chronos-RR",
        "H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert token in text
