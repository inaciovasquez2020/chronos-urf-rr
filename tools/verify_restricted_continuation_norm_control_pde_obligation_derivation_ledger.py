from __future__ import annotations

import json
from pathlib import Path

PREVIOUS_ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_norm_control_concrete_analytic_input_package_2026_06_14.json"
)
ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_norm_control_pde_obligation_derivation_ledger_2026_06_14.json"
)

REQUIRED_TOP_LEVEL = {
    "name": "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_OBLIGATION_DERIVATION_LEDGER",
    "status": "RUNALL_CONDITIONAL_PDE_OBLIGATION_DERIVATION_LEDGER",
    "target": "DERIVATION_OF_PACKAGE_OBLIGATIONS_FROM_RESTRICTED_CONTINUATION_PDE",
    "extends": "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_CONCRETE_ANALYTIC_INPUT_PACKAGE",
    "weakest_missing_object": "RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA",
    "first_admissible_subtarget": "RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA",
}

REQUIRED_OBJECTS = [
    "RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA",
    "RESTRICTED_CONTINUATION_FLUX_NONNEGATIVITY_LEMMA",
    "RESTRICTED_CONTINUATION_BOOTSTRAP_CLOSURE_LEMMA",
    "RESTRICTED_CONTINUATION_ESTIMATE_BRIDGE_AVAILABILITY_LEMMA",
]

REQUIRED_BOUNDARY = [
    "this artifact records the derivation ledger only",
    "this artifact does not prove the derivative identity",
    "this artifact does not prove flux nonnegativity",
    "this artifact does not prove bootstrap closure",
    "this artifact does not prove bridge availability",
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
        != "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_CONCRETE_ANALYTIC_INPUT_PACKAGE"
    ):
        raise SystemExit(f"MISSING_OBJECT := {PREVIOUS_ARTIFACT}:name")

    if (
        previous.get("weakest_missing_object")
        != "DERIVATION_OF_PACKAGE_OBLIGATIONS_FROM_RESTRICTED_CONTINUATION_PDE"
    ):
        raise SystemExit(f"MISSING_OBJECT := {PREVIOUS_ARTIFACT}:weakest_missing_object")

    for key, expected in REQUIRED_TOP_LEVEL.items():
        if data.get(key) != expected:
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:{key}")

    manifest = data.get("runall_target_manifest")
    if not isinstance(manifest, dict):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest")

    if manifest.get("TARGET") != "DERIVATION_OF_PACKAGE_OBLIGATIONS_FROM_RESTRICTED_CONTINUATION_PDE":
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGET")

    if (
        manifest.get("TARGETED_CHECK")
        != "python3 tools/verify_restricted_continuation_norm_control_pde_obligation_derivation_ledger.py"
    ):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGETED_CHECK")

    derivation_order = data.get("derivation_order")
    if not isinstance(derivation_order, list):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:derivation_order")

    if [entry.get("object") for entry in derivation_order] != REQUIRED_OBJECTS:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:derivation_order.objects")

    for index, entry in enumerate(derivation_order, start=1):
        if entry.get("step") != index:
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:derivation_order[{index}].step")
        if entry.get("status") != "missing":
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:derivation_order[{index}].status")
        for key in ["input", "output"]:
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:derivation_order[{index}].{key}")

    if data.get("boundary") != REQUIRED_BOUNDARY:
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:boundary")

    print("RUNALL_RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_OBLIGATION_DERIVATION_LEDGER_OK")


if __name__ == "__main__":
    main()
