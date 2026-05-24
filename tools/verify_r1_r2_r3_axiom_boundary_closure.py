from pathlib import Path
import json
import re

lean = Path("lean/Chronos/Frontier/R1R2R3AxiomBoundaryClosure.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/r1_r2_r3_axiom_boundary_closure_2026_05_24.json").read_text())
doc = Path("docs/status/R1_R2_R3_AXIOM_BOUNDARY_CLOSURE_2026_05_24.md").read_text()
root = Path("lean/Chronos.lean").read_text()

assert not re.search(r"(?m)^\s*axiom\b", lean)
assert not re.search(r"(?m)^\s*opaque\b", lean)

required_lean = [
    "R1FiniteDataToGeneralProofPromotionBridgeAssumption",
    "R2FiniteDataToGeneralProofPromotionBridgeAssumption",
    "R3FiniteDataToGeneralProofPromotionBridgeAssumption",
    "RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumption",
    "structure R1R2R3ConditionalAssumptionSurface",
    "R1FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface",
    "R2FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface",
    "R3FiniteDataToGeneralProofPromotionAssumption_conditional_on_surface",
    "RepositoryNativeR1R2R3InstanceTarget_conditional_on_surface",
    "NonFactorisationProofTarget_conditional_on_surface",
    "R1R2R3PromotionProofTargetRegistry_conditional_on_surface",
    "CONDITIONAL_ASSUMPTION_SURFACE_ONLY_NOT_CLOSURE",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "CONDITIONAL_ASSUMPTION_SURFACE_ONLY_NOT_CLOSURE"
assert artifact["closure_type"] == "NONE_CONDITIONAL_ASSUMPTION_SURFACE_ONLY"
assert artifact["assumption_surface"] == "R1R2R3ConditionalAssumptionSurface"
assert artifact["theorem_level_r1_closure"] is False
assert artifact["theorem_level_r2_closure"] is False
assert artifact["theorem_level_r3_closure"] is False
assert artifact["theorem_level_non_factorisation_closure"] is False
assert artifact["chronos_rr_closure"] is False
assert artifact["h4_1_fgl_closure"] is False
assert artifact["p_vs_np_closure"] is False
assert artifact["clay_problem_closure"] is False

for token in artifact["bridge_assumptions"]:
    assert token in lean, token
    assert token in doc, token

for token in artifact["conditional_surfaces"]:
    assert token in lean, token
    assert token in doc, token

for boundary in artifact["boundary"]:
    assert boundary in doc, boundary

assert "import Chronos.Frontier.R1R2R3AxiomBoundaryClosure" in root

print("R1/R2/R3 conditional assumption surface verified.")
