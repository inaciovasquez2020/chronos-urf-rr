#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/gravity_program_two_month_stop_lock_2026_06_28.json")

EXPECTED_STATUS = {
    "green_kernel_analytic_estimate_input_surface_percent": 76.5,
    "finite_jet_exclusion_estimate_component_isolation_percent": 68.0,
    "full_green_kernel_component_aggregate_surface_percent": 74.0,
    "boundary_documentation_validation_record_percent": 99.0,
    "full_green_kernel_estimates_proved_internally_percent": 0.0,
    "gravity_solved_percent": 0.0,
    "overall_gravity_program_maturity_percent": 33.1,
}

REQUIRED_FALSE = [
    ("classification", "finite_jet_aux_action_constructed_internally"),
    ("classification", "finite_jet_equivalence_witness_constructed_internally"),
    ("classification", "analytic_obligation_proved_internally"),
    ("classification", "full_green_kernel_estimates_proved_internally"),
    ("classification", "gravity_solved"),
    ("two_month_stop_lock", "count_local_unmerged_prs"),
    ("two_month_stop_lock", "allow_status_regression"),
    ("two_month_stop_lock", "allow_gravity_closure_claim"),
    ("two_month_stop_lock", "allow_green_kernel_internal_proof_claim"),
]

REQUIRED_TRUE = [
    ("classification", "finite_jet_aux_action_field_surface_exists"),
    ("classification", "finite_jet_aux_action_packaged_from_supplied_input"),
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["artifact"] == "gravity_program_two_month_stop_lock_2026_06_28"
    assert data["repository"] == "chronos-urf-rr"
    assert data["counted_head"] == "9bb24ace"
    assert data["counted_through_pr"] == 835
    assert data["weakest_point"] == "finite_jet_aux_action_internal_constructor"
    assert data["boundary"] == "BOUNDARY := ¬ internal_proof_of_Green_kernel_estimates"

    for key, expected in EXPECTED_STATUS.items():
        assert data["status"][key] == expected, f"{key} drifted"

    for section, key in REQUIRED_FALSE:
        assert data[section][key] is False, f"{section}.{key} must remain false"

    for section, key in REQUIRED_TRUE:
        assert data[section][key] is True, f"{section}.{key} must remain true"

    assert data["two_month_stop_lock"]["resume_point"] == "finite_jet_aux_action_internal_constructor"
    assert "FiniteJetCurvatureAuxAction" in data["two_month_stop_lock"]["next_admissible_object"]
    assert "returns or existentially produces FiniteJetCurvatureAuxAction" in data["two_month_stop_lock"]["internal_construction_counting_rule"]
    assert "does not prove Green-kernel estimates internally" in data["non_claims"]
    assert "does not solve gravity" in data["non_claims"]

    print("GRAVITY_PROGRAM_TWO_MONTH_STOP_LOCK_2026_06_28_OK")

if __name__ == "__main__":
    main()
