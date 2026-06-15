#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_formal_rr_theorem_proof_2026_06_15.json"
)

EXPECTED_ID = "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_FORMAL_RR_THEOREM_PROOF_TARGET"
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_FORMAL_RR_THEOREM_PROOF"
EXPECTED_PREDECESSOR = "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_RR_ROUTE_CLOSURE_GATE"
EXPECTED_STATUS = "THEOREM_PROOF_TARGET_ONLY_FORMAL_RR_THEOREM_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_ANALYTIC_ASSUMPTION_DISCHARGE_LEDGER"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    target = data["proof_target_statement"]
    assert target["name"] == "restricted_continuation_formal_rr_theorem_proof"

    required = target["required_inputs"]
    assert "restricted_continuation_rr_route_closure_gate_is_declared" in required
    assert "restricted_continuation_norm_control_theorem_payload_is_declared" in required
    assert "restricted_energy_identity_after_integration_by_parts" in required
    assert "boundary_flux_terms_are_classified_and_discharged" in required
    assert "interior_error_terms_are_controlled_or_absorbable" in required
    assert "energy_to_norm_control_transfer_is_available" in required
    assert "all_analytic_assumptions_used_by_the_route_are_declared" in required

    obligations = target["formal_proof_obligations"]
    assert len(obligations) == 4
    obligation_names = {obligation["obligation"] for obligation in obligations}
    assert obligation_names == {
        "route_gate_to_theorem_statement",
        "analytic_assumption_inventory",
        "lean_formalization_boundary",
        "full_rr_boundary_preservation",
    }

    intended = target["intended_conclusion"]
    assert "the_formal_rr_theorem_proof_target_is_declared" in intended
    assert "the_route_gate_has_a_theorem_level_proof_target" in intended
    assert (
        "all_remaining_analytic_assumption_discharge_requirements_are_made_explicit"
        in intended
    )
    assert (
        "analytic_assumption_discharge_ledger_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove the formal restricted-continuation theorem." in negative
    assert "Does not prove the norm-control theorem." in negative
    assert "Does not discharge all analytic assumptions in Lean." in negative
    assert "Does not close the RR restricted-continuation theorem." in negative
    assert "Does not close the full RR theorem." in negative
    assert "Does not claim final scientific closure." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_FORMAL_RR_THEOREM_PROOF_TARGET_OK")


if __name__ == "__main__":
    main()
