from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/R1R2R3AxiomBoundaryClosure.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/r1_r2_r3_axiom_boundary_closure_2026_05_24.json").read_text())
doc = Path("docs/status/R1_R2_R3_AXIOM_BOUNDARY_CLOSURE_2026_05_24.md").read_text()
root = Path("lean/Chronos.lean").read_text()

required_lean = [
    "axiom r1_finite_data_to_general_proof_promotion_axiom",
    "axiom r2_finite_data_to_general_proof_promotion_axiom",
    "axiom r3_finite_data_to_general_proof_promotion_axiom",
    "axiom repository_native_r1_r2_r3_instance_to_non_factorisation_axiom",
    "R1FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom",
    "R2FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom",
    "R3FiniteDataToGeneralProofPromotionAssumption_closed_by_axiom",
    "RepositoryNativeR1R2R3InstanceTarget_closed_by_axiom_boundary",
    "NonFactorisationProofTarget_closed_by_axiom_boundary",
    "R1R2R3PromotionProofTargetRegistry_closed_by_axiom_boundary",
    "CLOSED_BY_EXPLICIT_AXIOM_BOUNDARY_NOT_THEOREM_LEVEL",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "CLOSED_BY_EXPLICIT_AXIOM_BOUNDARY_NOT_THEOREM_LEVEL"
assert artifact["closure_type"] == "AXIOM_BOUNDARY"

for token in artifact["axioms"]:
    assert token in lean, token
    assert token in doc, token

for boundary in [
    "not theorem-level R1 closure",
    "not theorem-level R2 closure",
    "not theorem-level R3 closure",
    "not theorem-level NON_FACTORISATION closure",
    "no Chronos-RR closure",
    "no H4.1/FGL closure",
    "no P vs NP closure",
    "no Clay-problem closure",
]:
    assert boundary in artifact["boundary"], boundary
    assert boundary in doc, boundary

assert "import Chronos.Frontier.R1R2R3AxiomBoundaryClosure" in root

print("R1/R2/R3 axiom-boundary closure verified.")
