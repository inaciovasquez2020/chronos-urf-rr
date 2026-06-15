#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_regularitiy_and_differentiation_discharge_target_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_DISCHARGE_TARGET"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_DISCHARGE_TARGET"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_ANALYTIC_ASSUMPTION_DISCHARGE_LEDGER"
)
EXPECTED_STATUS = "DISCHARGE_TARGET_ONLY_REGULARITY_AND_DIFFERENTIATION_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_TIME_REGULAR_ENERGY_DISCHARGE_LEMMA"


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
        "restricted_continuation_regularity_and_differentiation_discharge_target"
    )
    assert target["assumption_group"] == "regularity_and_differentiation"

    assumptions = target["targeted_assumptions"]
    assert assumptions == [
        "solution_has_time_regular_energy",
        "solution_has_spatial_regularity_for_integration_by_parts",
        "energy_density_is_differentiable_along_restricted_continuation",
    ]

    obligations = target["discharge_obligations"]
    assert len(obligations) == 4
    obligation_names = {obligation["obligation"] for obligation in obligations}
    assert obligation_names == {
        "time_regular_energy",
        "spatial_regular_integration_by_parts",
        "energy_density_differentiability",
        "discharge_status_update",
    }

    intended = target["intended_conclusion"]
    assert (
        "the_regularitiy_and_differentiation_discharge_target_is_declared"
        in intended
    )
    assert (
        "the_first_analytic_assumption_group_has_a_concrete_discharge_target"
        in intended
    )
    assert (
        "no_regularitiy_or_differentiation_assumption_is_marked_as_discharged_without_proof"
        in intended
    )
    assert "time_regular_energy_discharge_lemma_is_now_the_next_required_check" in intended

    negative = data["claim"]["negative"]
    assert "Does not prove time-regular energy." in negative
    assert "Does not prove spatial regularity for integration by parts." in negative
    assert "Does not prove energy-density differentiability." in negative
    assert (
        "Does not discharge the regularity-and-differentiation assumption group."
        in negative
    )
    assert "Does not prove the formal restricted-continuation theorem." in negative
    assert "Does not close the full RR theorem." in negative

    print(
        "RUNALL_RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_DISCHARGE_TARGET_OK"
    )


if __name__ == "__main__":
    main()
