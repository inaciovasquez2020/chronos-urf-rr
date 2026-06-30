import json
import sys
from pathlib import Path

JSON_PATH = Path("artifacts/external_validation/gravity_program_closeout_boundary_2026_06_30.json")

REQUIRED_FALSE_GAPS = (
    "solved_gravity",
    "chronos_field_to_metric_action_map_proved",
    "einstein_equation_derived",
    "weak_field_limit_derived",
    "metric_backreaction_derived",
    "positive_carbon_gravity_mechanism_proved",
    "carbon_bonding_topology_independent_gravity_source_proved",
    "direct_diamond_graphite_eotvos_detection_claimed",
)

REQUIRED_TOP_LEVEL_BLOCKS = (
    "gravity_backreaction_reconstruction_boundary",
    "stress_energy_reduction_boundary",
    "carbon_structure_gravity_no_go_dichotomy",
    "diamond_graphite_experimental_boundary",
    "verifier_enforced_gaps",
)

def fail(message: str) -> None:
    print(f"VERIFIER ERROR: {message}")
    sys.exit(1)

def require_false(mapping: dict, key: str) -> None:
    if mapping.get(key) is not False:
        fail(f"'{key}' must be explicitly false.")

def main() -> None:
    if not JSON_PATH.exists():
        fail(f"Target file missing: {JSON_PATH}")

    data = json.loads(JSON_PATH.read_text())

    if data.get("metadata", {}).get("boundary") != "¬ solved_gravity":
        fail("metadata.boundary must be '¬ solved_gravity'.")

    if data.get("metadata", {}).get("final_missing_bridge") != "gravity_backreaction_reconstruction":
        fail("final missing bridge must remain gravity_backreaction_reconstruction.")

    for block in REQUIRED_TOP_LEVEL_BLOCKS:
        if block not in data:
            fail(f"Missing required block: {block}")

    gaps = data["verifier_enforced_gaps"]
    for key in REQUIRED_FALSE_GAPS:
        require_false(gaps, key)

    gravity = data["gravity_backreaction_reconstruction_boundary"]
    for key in (
        "chronos_to_metric_action_map_proved",
        "einstein_equation_derived",
        "weak_field_limit_derived",
        "metric_backreaction_derived",
    ):
        require_false(gravity, key)

    carbon = data["carbon_structure_gravity_no_go_dichotomy"]
    require_false(carbon, "carbon_bonding_topology_independent_gravity_source_proved")
    require_false(carbon, "positive_carbon_gravity_mechanism_proved")

    experiment = data["diamond_graphite_experimental_boundary"]
    require_false(experiment, "direct_diamond_graphite_eotvos_detection_claimed")
    require_false(experiment, "eta_diamond_graphite_realized")

    stress = data["stress_energy_reduction_boundary"]
    require_false(stress, "proved_as_full_physical_theorem")
    if stress.get("recorded_as_boundary") is not True:
        fail("stress-energy reduction must be recorded only as a boundary.")

    print("GRAVITY_PROGRAM_CLOSEOUT_BOUNDARY_OK")

if __name__ == "__main__":
    main()
