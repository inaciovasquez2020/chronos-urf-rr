import json
from pathlib import Path


def test_r1_r2_r3_axiom_boundary_closure_artifact():
    data = json.loads(
        Path("artifacts/chronos/r1_r2_r3_axiom_boundary_closure_2026_05_24.json").read_text()
    )
    assert data["status"] == "CLOSED_BY_EXPLICIT_AXIOM_BOUNDARY_NOT_THEOREM_LEVEL"
    assert data["closure_type"] == "AXIOM_BOUNDARY"
    assert len(data["axioms"]) == 4


def test_r1_r2_r3_axiom_boundary_closure_boundaries():
    text = Path("docs/status/R1_R2_R3_AXIOM_BOUNDARY_CLOSURE_2026_05_24.md").read_text()
    for token in [
        "not theorem-level R1 closure",
        "not theorem-level R2 closure",
        "not theorem-level R3 closure",
        "not theorem-level NON_FACTORISATION closure",
        "no Chronos-RR closure",
        "no H4.1/FGL closure",
        "no P vs NP closure",
        "no Clay-problem closure",
    ]:
        assert token in text


def test_r1_r2_r3_axiom_boundary_closure_lean_surface():
    text = Path("lean/Chronos/Frontier/R1R2R3AxiomBoundaryClosure.lean").read_text()
    for token in [
        "R1FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom",
        "R2FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom",
        "R3FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom",
        "NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_closed_by_axiom",
        "RepositoryNativeR1R2R3InstanceTarget_closed_by_axiom_boundary",
        "NonFactorisationProofTarget_closed_by_axiom_boundary",
        "R1R2R3PromotionProofTargetRegistry_closed_by_axiom_boundary",
    ]:
        assert token in text
