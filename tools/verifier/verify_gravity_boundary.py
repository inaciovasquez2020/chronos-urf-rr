import json
import sys
from pathlib import Path

JSON_PATH = Path("artifacts/external_validation/known_gravity_limit_interface_2026_06_29.json")

REQUIRED_FALSE_GAPS = (
    "einstein_limit_proved",
    "metric_backreaction_proved",
    "experimental_validation_proved",
    "stress_energy_realization_proved",
    "bridge_island_realization_proved",
    "lorentzian_metric_g_realization_proved",
    "stress_energy_T_realization_proved",
    "carbon_subplanck_gravity_containment_proved",
)

def fail(message: str) -> None:
    print(f"VERIFIER ERROR: {message}")
    sys.exit(1)

def main() -> None:
    if not JSON_PATH.exists():
        fail(f"Target file missing: {JSON_PATH}")

    data = json.loads(JSON_PATH.read_text())

    if data.get("metadata", {}).get("boundary") != "¬ solved_gravity":
        fail("Boundary configuration missing global invariant '¬ solved_gravity'.")

    gaps = data.get("verifier_enforced_gaps", {})
    for key in REQUIRED_FALSE_GAPS:
        if gaps.get(key) is not False:
            fail(f"'{key}' must be explicitly false.")

    bridge = data.get("bridge_island_configuration")
    if not isinstance(bridge, dict):
        fail("bridge_island_configuration must exist.")

    if bridge.get("object_name") != "ChronosGravityBridgeIsland":
        fail("bridge_island_configuration.object_name must be ChronosGravityBridgeIsland.")

    if bridge.get("implemented") is not False:
        fail("bridge_island_configuration must remain explicitly unimplemented.")

    stubs = data.get("interface_stubs", {})
    if not stubs:
        fail("interface_stubs must be nonempty.")

    for stub_name, properties in stubs.items():
        if properties.get("implemented") is not False:
            fail(f"Gravity limit stub '{stub_name}' cannot claim implementation.")

    print("KNOWN_GRAVITY_LIMIT_INTERFACE_BOUNDARY_OK")

if __name__ == "__main__":
    main()
