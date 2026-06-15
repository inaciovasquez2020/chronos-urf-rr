#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_trace_and_boundary_flux_discharge_target_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_TRACE_AND_BOUNDARY_FLUX_DISCHARGE_TARGET"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_TRACE_AND_BOUNDARY_FLUX_DISCHARGE_TARGET"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_GROUP_DISCHARGE_GATE"
)
EXPECTED_STATUS = "DISCHARGE_TARGET_ONLY_TRACE_AND_BOUNDARY_FLUX_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_BOUNDARY_TRACE_EXISTENCE_DISCHARGE_LEMMA"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    target = data["target_statement"]
    assert target["name"] == (
        "restricted_continuation_trace_and_boundary_flux_discharge_target"
    )
    assert target["assumption_group"] == "trace_and_boundary_flux"

    assumptions = target["targeted_assumptions"]
    assert assumptions == [
        "boundary_trace_exists_on_restricted_continuation_domain",
        "normal_trace_exists_for_flux_field",
        "trace_pairing_is_well_defined",
        "boundary_flux_pairing_well_defined_on_restricted_boundary",
    ]

    obligations = target["discharge_obligations"]
    assert len(obligations) == 5
    obligation_names = {obligation["obligation"] for obligation in obligations}
    assert obligation_names == {
        "boundary_trace_existence",
        "normal_trace_existence",
        "trace_pairing_well_defined",
        "boundary_flux_pairing_well_defined",
        "discharge_status_update_guard",
    }

    intended = target["intended_conclusion"]
    assert "the_trace_and_boundary_flux_discharge_target_is_declared" in intended
    assert (
        "the_second_analytic_assumption_group_has_a_concrete_discharge_target"
        in intended
    )
    assert (
        "no_trace_or_boundary_flux_assumption_is_marked_as_discharged_without_proof"
        in intended
    )
    assert (
        "boundary_trace_existence_discharge_lemma_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove boundary trace existence." in negative
    assert "Does not prove normal trace existence." in negative
    assert "Does not prove trace pairing well-definedness." in negative
    assert "Does not prove boundary flux pairing well-definedness." in negative
    assert (
        "Does not discharge the trace-and-boundary-flux assumption group."
        in negative
    )
    assert "Does not prove the formal restricted-continuation theorem." in negative
    assert "Does not close the full RR theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_TRACE_AND_BOUNDARY_FLUX_DISCHARGE_TARGET_OK")


if __name__ == "__main__":
    main()
