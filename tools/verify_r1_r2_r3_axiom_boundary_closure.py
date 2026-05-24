from pathlib import Path
import json
import re

lean = Path("lean/Chronos/Frontier/R1R2R3AxiomBoundaryClosure.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/r1_r2_r3_axiom_boundary_closure_2026_05_24.json").read_text())
doc = Path("docs/status/R1_R2_R3_AXIOM_BOUNDARY_CLOSURE_2026_05_24.md").read_text()
root = Path("lean/Chronos.lean").read_text()

assert not re.search(r"(?m)^\s*axiom\b", lean)

required_lean = [
    "opaque r1_finite_data_to_general_proof_promotion_assumption",
    "opaque r2_finite_data_to_general_proof_promotion_assumption",
    "opaque r3_finite_data_to_general_proof_promotion_assumption",
    "opaque repository_native_r1_r2_r3_instance_to_non_factorisation_assumption",
    "R1FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque",
    "R2FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque",
    "R3FiniteDataToGeneralProofPromotionAssumption_declared_by_opaque",
    "RepositoryNativeR1R2R3InstanceTarget_derived_under_opaque_boundary",
    "NonFactorisationProofTarget_derived_under_opaque_boundary",
    "R1R2R3PromotionProofTargetRegistry_derived_under_opaque_boundary",
    "OPAQUE_ASSUMPTION_DECLARATION_ONLY",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "OPAQUE_ASSUMPTION_DECLARATION_ONLY"
assert artifact["closure_type"] == "NONE_OPAQUE_BOUNDARY_ONLY"
assert artifact["theorem_level_r1_closure"] is False
assert artifact["theorem_level_r2_closure"] is False
assert artifact["theorem_level_r3_closure"] is False
assert artifact["theorem_level_non_factorisation_closure"] is False
assert artifact["chronos_rr_closure"] is False
assert artifact["h4_1_fgl_closure"] is False
assert artifact["p_vs_np_closure"] is False
assert artifact["clay_problem_closure"] is False

for token in artifact["opaque_assumptions"]:
    assert token in lean, token
    assert token in doc, token

for token in artifact["opaque_dependent_surfaces"]:
    assert token in lean, token
    assert token in doc, token

for boundary in artifact["boundary"]:
    assert boundary in doc, boundary

assert "import Chronos.Frontier.R1R2R3AxiomBoundaryClosure" in root

print("R1/R2/R3 opaque-boundary declaration verified.")
