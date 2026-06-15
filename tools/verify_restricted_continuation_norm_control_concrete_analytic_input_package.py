from __future__ import annotations

import json
from pathlib import Path

PREVIOUS_ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_norm_control_concrete_analytic_input_data_2026_06_14.json"
)
ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_norm_control_concrete_analytic_input_package_2026_06_14.json"
)

REQUIRED_TOP_LEVEL = {
    "name": "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_CONCRETE_ANALYTIC_INPUT_PACKAGE",
    "status": "RUNALL_CONDITIONAL_CONCRETE_ANALYTIC_INPUT_PACKAGE_DEFINED",
    "target": "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_PROOF",
    "extends": "RUNALL_VERIFIED_CONCRETE_RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_INPUT_DATA",
    "weakest_missing_object": "DERIVATION_OF_PACKAGE_OBLIGATIONS_FROM_RESTRICTED_CONTINUATION_PDE",
}

REQUIRED_PDE_KEYS = [
    "domain",
    "state",
    "evolution_equation",
    "initial_slice",
    "boundary_or_restriction_condition",
    "derivative_identity_obligation",
]

REQUIRED_ENERGY_KEYS = [
    "name",
    "definition",
    "controlled_norm",
    "finite_energy_regime",
    "analytic_estimate_target",
]

REQUIRED_FLUX_KEYS = [
    "flux_term",
    "sign",
    "normal_orientation",
    "nonnegative_flux_obligation",
]

REQUIRED_BOOTSTRAP_KEYS = [
    "bootstrap_bound",
    "source_bound",
    "coefficient_bound",
    "closure_obligation",
]

REQUIRED_BOUNDARY = [
    "this artifact defines the concrete analytic input package shape",
    "this artifact does not derive the derivative identity from the PDE",
    "this artifact does not prove flux nonnegativity",
    "this artifact does not prove bootstrap closure",
    "this artifact does not prove the analytic estimate",
    "this artifact does not prove full RR closure",
    "this artifact does not prove Clay problem closure",
]


def require_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"MISSING_OBJECT := {path}")
    return path.read_text(encoding="utf-8")


def require_mapping_keys(name: str, value: object, keys: list[str]) -> None:
    if not isinstance(value, dict):
        raise SystemExit(f"MISSING_OBJECT := {name}")

    for key in keys:
        if key not in value:
            raise SystemExit(f"MISSING_OBJECT := {name}.{key}")
        if not isinstance(value[key], str) or not value[key].strip():
            raise SystemExit(f"MISSING_OBJECT := {name}.{key}")


def main() -> None:
    previous_text = require_file(PREVIOUS_ARTIFACT)
    artifact_text = require_file(ARTIFACT)

    previous = json.loads(previous_text)
    data = json.loads(artifact_text)

    if (
        previous.get("name")
        != "RUNALL_VERIFIED_CONCRETE_RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_INPUT_DATA"
    ):
        raise SystemExit(f"MISSING_OBJECT := {PREVIOUS_ARTIFACT}:name")

    if (
        previous.get("weakest_missing_object")
        != "CONCRETE_RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_INPUT_DATA"
    ):
        raise SystemExit(f"MISSING_OBJECT := {PREVIOUS_ARTIFACT}:weakest_missing_object")

    for key, expected in REQUIRED_TOP_LEVEL.items():
        if data.get(key) != expected:
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:{key}")

    manifest = data.get("runall_target_manifest")
    if not isinstance(manifest, dict):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest")

    if manifest.get("TARGET") != "RESTRICTED_CONTINUATION_NORM_CONTROL_CONCRETE_ANALYTIC_INPUT_PACKAGE":
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGET")

    if (
        manifest.get("TARGETED_CHECK")
        != "python3 tools/verify_restricted_continuation_norm_control_concrete_analytic_input_package.py"
    ):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGETED_CHECK")

    require_mapping_keys(
        "concrete_pde_or_evolution_equations",
        data.get("concrete_pde_or_evolution_equations"),
        REQUIRED_PDE_KEYS,
    )
    require_mapping_keys(
        "energy_or_norm_functional",
        data.get("energy_or_norm_functional"),
        REQUIRED_ENERGY_KEYS,
    )
    require_mapping_keys(
        "flux_sign_convention",
        data.get("flux_sign_convention"),
        REQUIRED_FLUX_KEYS,
    )
    require_mapping_keys(
        "bootstrap_regime",
        data.get("bootstrap_regime"),
        REQUIRED_BOOTSTRAP_KEYS,
    )

    bridge = data.get("bridge_availability")
    if not isinstance(bridge, dict):
        raise SystemExit(f"MISSING_OBJECT := bridge_availability")

    required_payloads = bridge.get("required_payloads_after_this_package")
    if required_payloads != [
        "bridgeProofPayload",
        "derivativeIdentityProofPayload",
        "fluxNonnegativityProofPayload",
        "bootstrapBoundsProofPayload",
    ]:
        raise SystemExit("MISSING_OBJECT := bridge_availability.required_payloads_after_this_package")

    if data.get("boundary") != REQUIRED_BOUNDARY:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:boundary")

    print("RUNALL_RESTRICTED_CONTINUATION_NORM_CONTROL_CONCRETE_ANALYTIC_INPUT_PACKAGE_OK")


if __name__ == "__main__":
    main()
