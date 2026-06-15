#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_spatial_regularitiy_integration_by_parts_discharge_lemma_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_SPATIAL_REGULARITY_INTEGRATION_BY_PARTS_DISCHARGE_LEMMA"
)
EXPECTED_SOLVES = (
    "RESTRICTED_CONTINUATION_SPATIAL_REGULARITY_INTEGRATION_BY_PARTS_DISCHARGE_LEMMA"
)
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_TIME_REGULAR_ENERGY_DISCHARGE_LEMMA"
)
EXPECTED_STATUS = (
    "LEMMA_SURFACE_ONLY_SPATIAL_REGULARITY_INTEGRATION_BY_PARTS_NOT_PROVED"
)
EXPECTED_NEXT = (
    "RESTRICTED_CONTINUATION_ENERGY_DENSITY_DIFFERENTIABILITY_DISCHARGE_LEMMA"
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
    assert lemma["name"] == (
        "restricted_continuation_spatial_regularity_integration_by_parts_discharge"
    )
    assert lemma["assumption_group"] == "regularity_and_differentiation"
    assert lemma["targeted_assumption"] == (
        "solution_has_spatial_regularity_for_integration_by_parts"
    )

    required = lemma["required_inputs"]
    assert "restricted_continuation_domain_is_declared" in required
    assert "solution_spatial_regular_representative_is_available" in required
    assert "weak_gradient_or_flux_field_is_defined" in required
    assert "integration_by_parts_pairing_is_well_defined" in required
    assert "boundary_trace_or_flux_pairing_interface_is_declared" in required

    obligations = lemma["discharge_obligations"]
    assert len(obligations) == 5
    obligation_names = {obligation["obligation"] for obligation in obligations}
    assert obligation_names == {
        "restricted_domain_spatial_structure",
        "solution_spatial_regular_representative",
        "weak_gradient_flux_admissibility",
        "boundary_pairing_interface",
        "ledger_status_update_guard",
    }

    intended = lemma["intended_conclusion"]
    assert (
        "the_spatial_regularity_integration_by_parts_discharge_lemma_target_is_declared"
        in intended
    )
    assert (
        "the_spatial_regularity_assumption_has_a_dedicated_discharge_surface"
        in intended
    )
    assert (
        "no_spatial_regularity_assumption_is_marked_as_discharged_without_proof"
        in intended
    )
    assert (
        "energy_density_differentiability_discharge_lemma_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove spatial regularity for integration by parts." in negative
    assert "Does not prove existence of a spatially regular representative." in negative
    assert "Does not prove weak-gradient or flux admissibility." in negative
    assert "Does not prove boundary trace or flux pairing." in negative
    assert (
        "Does not discharge the regularity-and-differentiation assumption group."
        in negative
    )
    assert "Does not prove the formal restricted-continuation theorem." in negative
    assert "Does not close the full RR theorem." in negative

    print(
        "RUNALL_RESTRICTED_CONTINUATION_SPATIAL_REGULARITY_INTEGRATION_BY_PARTS_DISCHARGE_LEMMA_OK"
    )


if __name__ == "__main__":
    main()
