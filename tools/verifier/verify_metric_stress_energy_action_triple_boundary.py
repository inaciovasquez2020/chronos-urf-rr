import json
import sys
from pathlib import Path

JSON_PATH = Path("artifacts/external_validation/metric_stress_energy_action_triple_boundary_2026_06_30.json")

REQUIRED_FALSE_GAPS = (
    "ChronosFieldObject_constructs_metric_stress_energy_action_triple",
    "lorentzian_metric_g_derived",
    "stress_energy_T_derived",
    "action_functional_derived",
    "nontrivial_metric_stress_energy_action_coupling_proved",
    "einstein_equation_derived",
    "metric_backreaction_derived",
    "solved_gravity",
)

REQUIRED_COMPONENT_FALSE = (
    "LorentzianMetric.g_derived_from_ChronosFieldObject",
    "StressEnergyTensor.T_derived_from_ChronosFieldObject",
    "ActionFunctional_derived_from_ChronosFieldObject",
    "nontrivial_metric_stress_energy_action_coupling_proved",
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

    if data.get("metadata", {}).get("boundary") != "¬ ChronosFieldObject_constructs_metric_stress_energy_action_triple":
        fail("metadata.boundary must preserve the ChronosFieldObject triple non-construction boundary.")

    triple = data.get("target_triple")
    if not isinstance(triple, dict):
        fail("target_triple block must exist.")

    if triple.get("object_name") != "MetricStressEnergyActionTriple":
        fail("target_triple.object_name must be MetricStressEnergyActionTriple.")

    if triple.get("source") != "ChronosFieldObject":
        fail("target_triple.source must be ChronosFieldObject.")

    if triple.get("A_target_name") != "ActionFunctional":
        fail("A target must be fixed as ActionFunctional.")

    components = data.get("component_status")
    if not isinstance(components, dict):
        fail("component_status block must exist.")

    for key in REQUIRED_COMPONENT_FALSE:
        require_false(components, key)

    gaps = data.get("verifier_enforced_gaps")
    if not isinstance(gaps, dict):
        fail("verifier_enforced_gaps block must exist.")

    for key in REQUIRED_FALSE_GAPS:
        require_false(gaps, key)

    print("METRIC_STRESS_ENERGY_ACTION_TRIPLE_BOUNDARY_OK")

if __name__ == "__main__":
    main()
