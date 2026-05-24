import json
import re
from pathlib import Path


def test_r1_r2_r3_conditional_assumption_surface_artifact():
    data = json.loads(
        Path("artifacts/chronos/r1_r2_r3_axiom_boundary_closure_2026_05_24.json").read_text()
    )
    assert data["status"] == "CONDITIONAL_ASSUMPTION_SURFACE_ONLY_NOT_CLOSURE"
    assert data["closure_type"] == "NONE_CONDITIONAL_ASSUMPTION_SURFACE_ONLY"
    assert data["assumption_surface"] == "R1R2R3ConditionalAssumptionSurface"
    assert len(data["bridge_assumptions"]) == 4
    assert data["theorem_level_r1_closure"] is False
    assert data["theorem_level_r2_closure"] is False
    assert data["theorem_level_r3_closure"] is False
    assert data["theorem_level_non_factorisation_closure"] is False
    assert data["chronos_rr_closure"] is False
    assert data["h4_1_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False
    assert data["clay_problem_closure"] is False


def test_r1_r2_r3_conditional_assumption_surface_boundaries():
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


def test_r1_r2_r3_conditional_assumption_surface_lean_surface():
    text = Path("lean/Chronos/Frontier/R1R2R3AxiomBoundaryClosure.lean").read_text()
    assert not re.search(r"(?m)^\\s*axiom\\b", text)
    assert not re.search(r"(?m)^\\s*opaque\\b", text)
    for token in [
        "R1FiniteDataToGeneralProofPromotionBridgeAssumption",
        "R2FiniteDataToGeneralProofPromotionBridgeAssumption",
        "R3FiniteDataToGeneralProofPromotionBridgeAssumption",
        "RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumption",
        "R1R2R3ConditionalAssumptionSurface",
        "RepositoryNativeR1R2R3InstanceTarget_conditional_on_surface",
        "NonFactorisationProofTarget_conditional_on_surface",
        "R1R2R3PromotionProofTargetRegistry_conditional_on_surface",
        "CONDITIONAL_ASSUMPTION_SURFACE_ONLY_NOT_CLOSURE",
    ]:
        assert token in text
