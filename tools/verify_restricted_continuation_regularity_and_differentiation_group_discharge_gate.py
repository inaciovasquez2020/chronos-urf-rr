#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_regularity_and_differentiation_group_discharge_gate_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_GROUP_DISCHARGE_GATE"
)
EXPECTED_SOLVES = (
    "RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_GROUP_DISCHARGE_GATE"
)
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_ENERGY_DENSITY_DIFFERENTIABILITY_DISCHARGE_LEMMA"
)
EXPECTED_STATUS = (
    "GATE_SURFACE_ONLY_REGULARITY_AND_DIFFERENTIATION_GROUP_NOT_DISCHARGED"
)
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_TRACE_AND_BOUNDARY_FLUX_DISCHARGE_TARGET"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    gate = data["gate_statement"]
    assert gate["name"] == (
        "restricted_continuation_regularity_and_differentiation_group_discharge_gate"
    )
    assert gate["assumption_group"] == "regularity_and_differentiation"

    required = gate["required_inputs"]
    assert "time_regular_energy_discharge_lemma_target_is_declared" in required
    assert (
        "spatial_regularity_integration_by_parts_discharge_lemma_target_is_declared"
        in required
    )
    assert (
        "energy_density_differentiability_discharge_lemma_target_is_declared"
        in required
    )
    assert "regularity_and_differentiation_ledger_group_is_visible" in required
    assert (
        "no_regularitiy_or_differentiation_assumption_is_marked_as_discharged_without_proof"
        in required
    )

    checks = gate["gate_checks"]
    assert len(checks) == 4
    check_names = {check["check"] for check in checks}
    assert check_names == {
        "time_regular_energy_obligation_visible",
        "spatial_regular_ibp_obligation_visible",
        "energy_density_differentiability_obligation_visible",
        "undischarged_group_boundary_preserved",
    }

    intended = gate["intended_conclusion"]
    assert (
        "the_regularity_and_differentiation_group_discharge_gate_is_declared"
        in intended
    )
    assert (
        "all_three_regularity_and_differentiation_discharge_targets_are_visible"
        in intended
    )
    assert (
        "the_regularitiy_and_differentiation_group_remains_not_discharged_without_proof"
        in intended
    )
    assert (
        "trace_and_boundary_flux_discharge_target_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert (
        "Does not discharge the regularity-and-differentiation assumption group."
        in negative
    )
    assert "Does not prove time-regular energy." in negative
    assert "Does not prove spatial regularity for integration by parts." in negative
    assert "Does not prove energy-density differentiability." in negative
    assert "Does not prove trace existence or boundary flux pairing." in negative
    assert "Does not prove the formal restricted-continuation theorem." in negative
    assert "Does not close the full RR theorem." in negative

    print(
        "RUNALL_RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_GROUP_DISCHARGE_GATE_OK"
    )


if __name__ == "__main__":
    main()
