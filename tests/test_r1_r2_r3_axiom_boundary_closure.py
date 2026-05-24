import json
import re
from pathlib import Path


def test_r1_r2_r3_opaque_boundary_declaration_artifact():
    data = json.loads(
        Path("artifacts/chronos/r1_r2_r3_axiom_boundary_closure_2026_05_24.json").read_text()
    )
    assert data["status"] == "OPAQUE_ASSUMPTION_DECLARATION_ONLY"
    assert data["closure_type"] == "NONE_OPAQUE_BOUNDARY_ONLY"
    assert len(data["opaque_assumptions"]) == 4
    assert data["theorem_level_r1_closure"] is False
    assert data["theorem_level_r2_closure"] is False
    assert data["theorem_level_r3_closure"] is False
    assert data["theorem_level_non_factorisation_closure"] is False
    assert data["chronos_rr_closure"] is False
    assert data["h4_1_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False
    assert data["clay_problem_closure"] is False


def test_r1_r2_r3_opaque_boundary_declaration_boundaries():
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


def test_r1_r2_r3_opaque_boundary_declaration_lean_surface():
    text = Path("lean/Chronos/Frontier/R1R2R3AxiomBoundaryClosure.lean").read_text()
    assert not re.search(r"(?m)^\\s*axiom\\b", text)
    for token in [
        "R1FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque",
        "R2FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque",
        "R3FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque",
        "NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance_declared_by_opaque",
        "RepositoryNativeR1R2R3InstanceTarget_derived_under_opaque_boundary",
        "NonFactorisationProofTarget_derived_under_opaque_boundary",
        "R1R2R3PromotionProofTargetRegistry_derived_under_opaque_boundary",
        "OPAQUE_ASSUMPTION_DECLARATION_ONLY",
    ]:
        assert token in text
