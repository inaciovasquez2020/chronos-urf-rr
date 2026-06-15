#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_time_regular_energy_discharge_lemma_2026_06_15.json"
)

EXPECTED_ID = "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_TIME_REGULAR_ENERGY_DISCHARGE_LEMMA"
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_TIME_REGULAR_ENERGY_DISCHARGE_LEMMA"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_DISCHARGE_TARGET"
)
EXPECTED_STATUS = "LEMMA_SURFACE_ONLY_TIME_REGULAR_ENERGY_NOT_PROVED"
EXPECTED_NEXT = (
    "RESTRICTED_CONTINUATION_SPATIAL_REGULARITY_INTEGRATION_BY_PARTS_DISCHARGE_LEMMA"
)


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    lemma = data["lemma_statement"]
    assert lemma["name"] == "restricted_continuation_time_regular_energy_discharge"
    assert lemma["assumption_group"] == "regularity_and_differentiation"
    assert lemma["targeted_assumption"] == "solution_has_time_regular_energy"

    required = lemma["required_inputs"]
    assert "restricted_continuation_energy_functional_is_well_defined" in required
    assert "restricted_continuation_time_parameter_is_declared" in required
    assert (
        "energy_along_restricted_continuation_is_defined_for_the_target_time_interval"
        in required
    )
    assert (
        "time_regular_representative_or_weak_derivative_payload_is_available"
        in required
    )

    obligations = lemma["discharge_obligations"]
    assert len(obligations) == 4
    obligation_names = {obligation["obligation"] for obligation in obligations}
    assert obligation_names == {
        "energy_time_domain",
        "energy_time_regular_representative",
        "energy_derivative_admissibility",
        "ledger_status_update_guard",
    }

    intended = lemma["intended_conclusion"]
    assert "the_time_regular_energy_discharge_lemma_target_is_declared" in intended
    assert "the_time_regular_energy_assumption_has_a_dedicated_discharge_surface" in intended
    assert (
        "no_time_regular_energy_assumption_is_marked_as_discharged_without_proof"
        in intended
    )
    assert (
        "spatial_regular_integration_by_parts_discharge_lemma_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove time-regular energy." in negative
    assert "Does not prove existence of a time-regular representative." in negative
    assert "Does not prove energy derivative admissibility." in negative
    assert (
        "Does not discharge the regularity-and-differentiation assumption group."
        in negative
    )
    assert "Does not prove the formal restricted-continuation theorem." in negative
    assert "Does not close the full RR theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_TIME_REGULAR_ENERGY_DISCHARGE_LEMMA_OK")


if __name__ == "__main__":
    main()
