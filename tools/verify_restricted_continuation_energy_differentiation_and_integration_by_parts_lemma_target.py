from __future__ import annotations

import json
from pathlib import Path

PREVIOUS_ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_norm_control_pde_to_derivative_identity_lemma_target_2026_06_15.json"
)
ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_energy_differentiation_and_integration_by_parts_lemma_target_2026_06_15.json"
)

REQUIRED_TOP_LEVEL = {
    "name": "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_ENERGY_DIFFERENTIATION_AND_INTEGRATION_BY_PARTS_LEMMA_TARGET",
    "status": "RUNALL_CONDITIONAL_ENERGY_DIFFERENTIATION_AND_INTEGRATION_BY_PARTS_LEMMA_TARGET",
    "target": "RESTRICTED_CONTINUATION_ENERGY_DIFFERENTIATION_AND_INTEGRATION_BY_PARTS_LEMMA",
    "extends": "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA_TARGET",
    "weakest_missing_object": "RESTRICTED_CONTINUATION_REGULARITY_TRACE_AND_BOUNDARY_FLUX_ASSUMPTIONS",
    "first_admissible_subtarget": "RESTRICTED_CONTINUATION_REGULARITY_TRACE_AND_BOUNDARY_FLUX_ASSUMPTIONS",
}

REQUIRED_STATEMENT_KEYS = [
    "input_region",
    "state_regularization",
    "energy_functional",
    "differentiation_target",
    "integration_by_parts_target",
    "shared_boundary_convention",
    "output_for_derivative_identity",
]

REQUIRED_BLOCKS = [
    "RESTRICTED_CONTINUATION_TIME_REGULARITY_BLOCK",
    "RESTRICTED_CONTINUATION_SPATIAL_REGULARITY_BLOCK",
    "RESTRICTED_CONTINUATION_TRACE_BLOCK",
    "RESTRICTED_CONTINUATION_OPERATOR_SYMMETRY_OR_DIVERGENCE_BLOCK",
    "RESTRICTED_CONTINUATION_BOUNDARY_FLUX_DEFINITION_BLOCK",
]

REQUIRED_BOUNDARY = [
    "this artifact records the energy differentiation and integration-by-parts lemma target only",
    "this artifact does not prove time regularity",
    "this artifact does not prove spatial regularity",
    "this artifact does not prove boundary trace existence",
    "this artifact does not prove integration by parts",
    "this artifact does not prove boundary flux identification",
    "this artifact does not prove the derivative identity",
    "this artifact does not prove the analytic estimate",
    "this artifact does not prove full RR closure",
    "this artifact does not prove Clay problem closure",
]


def require_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"MISSING_OBJECT := {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    previous = json.loads(require_file(PREVIOUS_ARTIFACT))
    data = json.loads(require_file(ARTIFACT))

    if (
        previous.get("name")
        != "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA_TARGET"
    ):
        raise SystemExit(f"MISSING_OBJECT := {PREVIOUS_ARTIFACT}:name")

    if (
        previous.get("weakest_missing_object")
        != "RESTRICTED_CONTINUATION_ENERGY_DIFFERENTIATION_AND_INTEGRATION_BY_PARTS_LEMMA"
    ):
        raise SystemExit(f"MISSING_OBJECT := {PREVIOUS_ARTIFACT}:weakest_missing_object")

    for key, expected in REQUIRED_TOP_LEVEL.items():
        if data.get(key) != expected:
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:{key}")

    manifest = data.get("runall_target_manifest")
    if not isinstance(manifest, dict):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest")

    if manifest.get("TARGET") != "RESTRICTED_CONTINUATION_ENERGY_DIFFERENTIATION_AND_INTEGRATION_BY_PARTS_LEMMA":
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGET")

    if (
        manifest.get("TARGETED_CHECK")
        != "python3 tools/verify_restricted_continuation_energy_differentiation_and_integration_by_parts_lemma_target.py"
    ):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGETED_CHECK")

    statement = data.get("lemma_statement_surface")
    if not isinstance(statement, dict):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:lemma_statement_surface")

    for key in REQUIRED_STATEMENT_KEYS:
        if not isinstance(statement.get(key), str) or not statement[key].strip():
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:lemma_statement_surface.{key}")

    if "d/dt E_R(t)" not in statement["differentiation_target"]:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:lemma_statement_surface.differentiation_target")

    if "Flux_R(t)" not in statement["integration_by_parts_target"]:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:lemma_statement_surface.integration_by_parts_target")

    blocks = data.get("required_assumption_blocks")
    if not isinstance(blocks, list):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:required_assumption_blocks")

    if [entry.get("object") for entry in blocks] != REQUIRED_BLOCKS:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:required_assumption_blocks.objects")

    for index, entry in enumerate(blocks, start=1):
        if entry.get("status") != "missing":
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:required_assumption_blocks[{index}].status")
        if not isinstance(entry.get("role"), str) or not entry["role"].strip():
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:required_assumption_blocks[{index}].role")

    if data.get("boundary") != REQUIRED_BOUNDARY:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:boundary")

    print("RUNALL_RESTRICTED_CONTINUATION_ENERGY_DIFFERENTIATION_AND_INTEGRATION_BY_PARTS_LEMMA_TARGET_OK")


if __name__ == "__main__":
    main()
