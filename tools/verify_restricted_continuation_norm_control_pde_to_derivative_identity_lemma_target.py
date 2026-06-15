from __future__ import annotations

import json
from pathlib import Path

PREVIOUS_ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_norm_control_pde_obligation_derivation_ledger_2026_06_14.json"
)
ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_norm_control_pde_to_derivative_identity_lemma_target_2026_06_15.json"
)

REQUIRED_TOP_LEVEL = {
    "name": "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA_TARGET",
    "status": "RUNALL_CONDITIONAL_DERIVATIVE_IDENTITY_LEMMA_TARGET",
    "target": "RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA",
    "extends": "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_OBLIGATION_DERIVATION_LEDGER",
    "weakest_missing_object": "RESTRICTED_CONTINUATION_ENERGY_DIFFERENTIATION_AND_INTEGRATION_BY_PARTS_LEMMA",
    "first_admissible_subtarget": "RESTRICTED_CONTINUATION_ENERGY_DIFFERENTIATION_AND_INTEGRATION_BY_PARTS_LEMMA",
}

REQUIRED_STATEMENT_KEYS = [
    "input_equation",
    "energy",
    "target_identity",
    "region",
    "boundary_convention",
    "shared_input_surface",
]

REQUIRED_COMPONENTS = [
    "ENERGY_DIFFERENTIABILITY_LEMMA",
    "PDE_SUBSTITUTION_LEMMA",
    "RESTRICTED_INTEGRATION_BY_PARTS_LEMMA",
    "LOWER_ORDER_TERM_ABSORPTION_LEMMA",
    "DERIVATIVE_IDENTITY_ASSEMBLY_LEMMA",
]

REQUIRED_BOUNDARY = [
    "this artifact records the derivative identity lemma target only",
    "this artifact does not prove energy differentiability",
    "this artifact does not prove PDE substitution",
    "this artifact does not prove restricted integration by parts",
    "this artifact does not prove lower-order term absorption",
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
        != "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_OBLIGATION_DERIVATION_LEDGER"
    ):
        raise SystemExit(f"MISSING_OBJECT := {PREVIOUS_ARTIFACT}:name")

    if (
        previous.get("weakest_missing_object")
        != "RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA"
    ):
        raise SystemExit(f"MISSING_OBJECT := {PREVIOUS_ARTIFACT}:weakest_missing_object")

    for key, expected in REQUIRED_TOP_LEVEL.items():
        if data.get(key) != expected:
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:{key}")

    manifest = data.get("runall_target_manifest")
    if not isinstance(manifest, dict):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest")

    if manifest.get("TARGET") != "RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA":
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGET")

    if (
        manifest.get("TARGETED_CHECK")
        != "python3 tools/verify_restricted_continuation_norm_control_pde_to_derivative_identity_lemma_target.py"
    ):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGETED_CHECK")

    statement = data.get("lemma_statement_surface")
    if not isinstance(statement, dict):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:lemma_statement_surface")

    for key in REQUIRED_STATEMENT_KEYS:
        if not isinstance(statement.get(key), str) or not statement[key].strip():
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:lemma_statement_surface.{key}")

    if "d/dt E_R(t) + Flux_R(t) <= Source_R(t)" not in statement["target_identity"]:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:lemma_statement_surface.target_identity")

    components = data.get("required_derivation_components")
    if not isinstance(components, list):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:required_derivation_components")

    if [entry.get("object") for entry in components] != REQUIRED_COMPONENTS:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:required_derivation_components.objects")

    for index, entry in enumerate(components, start=1):
        if entry.get("status") != "missing":
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:required_derivation_components[{index}].status")
        if not isinstance(entry.get("role"), str) or not entry["role"].strip():
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:required_derivation_components[{index}].role")

    if data.get("boundary") != REQUIRED_BOUNDARY:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:boundary")

    print("RUNALL_RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA_TARGET_OK")


if __name__ == "__main__":
    main()
