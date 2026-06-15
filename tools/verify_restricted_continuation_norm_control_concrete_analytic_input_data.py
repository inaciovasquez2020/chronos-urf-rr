from __future__ import annotations

import json
from pathlib import Path

INPUT_SURFACE = Path(
    "lean/Chronos/Frontier/RestrictedContinuationNormControlAnalyticEstimateInputSurface.lean"
)
PAYLOAD_SURFACE = Path(
    "lean/Chronos/Frontier/RestrictedContinuationNormControlPayloadFieldProofPayloads.lean"
)
PREVIOUS_ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_norm_control_payload_field_proof_payloads_2026_06_13.json"
)
ARTIFACT = Path(
    "artifacts/chronos/restricted_continuation_norm_control_concrete_analytic_input_data_2026_06_14.json"
)

REQUIRED_INPUT_SURFACE_MARKERS = [
    "structure RestrictedContinuationNormControlAnalyticEstimateInputData where",
    "proofBridgeData : RestrictedContinuationNormControlEstimateProofBridgeData",
    "derivativeIdentityInput : Prop",
    "fluxNonnegativityInput : Prop",
    "bootstrapBoundsInput : Prop",
    "analyticEstimateInput : Prop",
    "def RestrictedContinuationNormControlAnalyticEstimateInputObligation",
    "theorem RestrictedContinuationNormControlAnalyticEstimateInputSurface",
]

REQUIRED_PAYLOAD_SURFACE_MARKERS = [
    "structure RestrictedContinuationNormControlPayloadFieldProofPayloadsHypotheses where",
    "bridgeProofPayload",
    "derivativeIdentityProofPayload",
    "fluxNonnegativityProofPayload",
    "bootstrapBoundsProofPayload",
    "RestrictedContinuationNormControlPayloadFieldProofPayloadsStopBoundary",
    "STOP_AFTER_THIS_COMMIT_NO_ADMISSIBLE_NEXT_STEP_WITHOUT_NEW_ANALYTIC_INPUT",
]

REQUIRED_ARTIFACT_FIELDS = {
    "name": "RUNALL_VERIFIED_CONCRETE_RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_INPUT_DATA",
    "status": "RUNALL_CONDITIONAL_CONCRETE_ANALYTIC_INPUT_DATA_BOUNDARY",
    "target": "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_PROOF",
    "weakest_missing_object": "CONCRETE_RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_INPUT_DATA",
    "previous_verified_boundary": "STOP_AFTER_THIS_COMMIT_NO_ADMISSIBLE_NEXT_STEP_WITHOUT_NEW_ANALYTIC_INPUT",
}

REQUIRED_CONCRETE_FIELDS = [
    "restricted_continuation_pde_or_evolution_equations",
    "energy_or_norm_functional",
    "flux_term_and_sign_convention",
    "bootstrap_regime_and_bounds",
    "analytic_estimate_target",
    "estimate_proof_bridge_availability",
]

REQUIRED_PROP_FIELDS = [
    "derivativeIdentityInput",
    "fluxNonnegativityInput",
    "bootstrapBoundsInput",
    "analyticEstimateInput",
]

REQUIRED_PAYLOADS = [
    "bridgeProofPayload",
    "derivativeIdentityProofPayload",
    "fluxNonnegativityProofPayload",
    "bootstrapBoundsProofPayload",
]

REQUIRED_BOUNDARIES = [
    "this artifact does not prove the analytic estimate",
    "this artifact does not prove derivative identity from PDE equations",
    "this artifact does not prove flux nonnegativity from PDE equations",
    "this artifact does not prove bootstrap bounds",
    "this artifact does not prove full RR closure",
    "this artifact does not prove Clay problem closure",
]


def require_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"MISSING_OBJECT := {path}")
    return path.read_text(encoding="utf-8")


def require_marker(text: str, marker: str, source: Path) -> None:
    if marker not in text:
        raise SystemExit(f"MISSING_OBJECT := {source}:{marker}")


def require_list(name: str, got: object, expected: list[str]) -> None:
    if got != expected:
        raise SystemExit(f"MISSING_OBJECT := {name}")


def main() -> None:
    input_surface_text = require_file(INPUT_SURFACE)
    payload_surface_text = require_file(PAYLOAD_SURFACE)
    previous_artifact_text = require_file(PREVIOUS_ARTIFACT)
    artifact_text = require_file(ARTIFACT)

    for marker in REQUIRED_INPUT_SURFACE_MARKERS:
        require_marker(input_surface_text, marker, INPUT_SURFACE)

    for marker in REQUIRED_PAYLOAD_SURFACE_MARKERS:
        require_marker(payload_surface_text, marker, PAYLOAD_SURFACE)

    require_marker(
        previous_artifact_text,
        '"stop_boundary": "STOP_AFTER_THIS_COMMIT_NO_ADMISSIBLE_NEXT_STEP_WITHOUT_NEW_ANALYTIC_INPUT"',
        PREVIOUS_ARTIFACT,
    )

    data = json.loads(artifact_text)

    for key, expected in REQUIRED_ARTIFACT_FIELDS.items():
        if data.get(key) != expected:
            raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:{key}")

    require_list(
        "concrete_input_data_required_fields",
        data.get("concrete_input_data_required_fields"),
        REQUIRED_CONCRETE_FIELDS,
    )
    require_list(
        "current_abstract_prop_fields_requiring_concrete_content",
        data.get("current_abstract_prop_fields_requiring_concrete_content"),
        REQUIRED_PROP_FIELDS,
    )
    require_list(
        "required_future_payloads",
        data.get("required_future_payloads"),
        REQUIRED_PAYLOADS,
    )
    require_list("boundary", data.get("boundary"), REQUIRED_BOUNDARIES)

    manifest = data.get("runall_target_manifest")
    if not isinstance(manifest, dict):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest")

    if manifest.get("TARGET") != "CONCRETE_RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_INPUT_DATA":
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGET")

    if (
        manifest.get("TARGETED_CHECK")
        != "python3 tools/verify_restricted_continuation_norm_control_concrete_analytic_input_data.py"
    ):
        raise SystemExit(f"MISSING_OBJECT := {ARTIFACT}:runall_target_manifest.TARGETED_CHECK")

    print("RUNALL_CONCRETE_RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_INPUT_DATA_BOUNDARY_OK")


if __name__ == "__main__":
    main()
