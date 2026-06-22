import json
from pathlib import Path

artifact_path = Path("artifacts/chronos/r1_native_map_conditional_contract_constructor_status_2026_06_22.json")
doc_path = Path("docs/status/R1_NATIVE_MAP_CONDITIONAL_CONTRACT_CONSTRUCTOR_STATUS.md")
lean_path = Path("lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContractFromTargets.lean")
constructor_verifier = Path("tools/verify_r1_native_map_input_contract_conditional_constructor_from_targets.py")
rank_artifact = Path("artifacts/chronos/r1_native_map_remaining_evidence_obligation_rank_2026_06_22.json")

for path in [artifact_path, doc_path, lean_path, constructor_verifier, rank_artifact]:
    if not path.exists():
        raise SystemExit(f"MISSING_OBJECT := {path}")

artifact = json.loads(artifact_path.read_text())
doc = doc_path.read_text()
lean = lean_path.read_text()
constructor_verifier_text = constructor_verifier.read_text()
rank = json.loads(rank_artifact.read_text())

required_artifact = {
    "status": "R1_NATIVE_MAP_CONDITIONAL_CONTRACT_CONSTRUCTOR_STATUS",
    "input_head": "dc451809",
    "constructor": "r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets",
    "aligned_input_shape": "R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets",
    "constructor_status": "conditional_constructor_only",
    "full_native_map_input_contract_discharged": False,
    "unconditional_non_factorization_theorem_proved": False,
}

for key, expected in required_artifact.items():
    if artifact.get(key) != expected:
        raise SystemExit(f"MISSING_OBJECT := artifact.{key}")

required_tokens = [
    "R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets",
    "r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets",
    "R1ConcreteNewsteinFGLToNativeMapInputContract D where",
    "R1LongChordExclusionDischargeTarget",
    "R1DiameterSeparationFillingObstructionDischargeTarget",
    "R1UniformLocalTypeCapacityDischargeTarget",
    "R1SourceToNativeCompatibilityDischargeTarget",
    "r1_native_map_input_contract_from_aligned_targets_long_chord_eq",
    "r1_native_map_input_contract_from_aligned_targets_diameter_eq",
    "r1_native_map_input_contract_from_aligned_targets_uniform_eq",
    "r1_native_map_input_contract_from_aligned_targets_compatibility_eq",
    "R1_NATIVE_MAP_INPUT_CONTRACT_CONDITIONAL_CONSTRUCTOR_FROM_TARGETS_OK",
    "The full native-map input contract is not discharged unconditionally.",
    "The unconditional non-factorization theorem is not proved.",
    "compatibility invariant evidence",
    "diameter-separation filling-obstruction evidence",
    "uniform local-type capacity evidence",
]

haystack = "\n".join([
    json.dumps(artifact, sort_keys=True),
    doc,
    lean,
    constructor_verifier_text,
    json.dumps(rank, sort_keys=True),
])

missing = [token for token in required_tokens if token not in haystack]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

if len(artifact.get("requires_existing_evidence_targets", [])) != 4:
    raise SystemExit("MISSING_OBJECT := four_required_evidence_targets")
if len(artifact.get("preserved_target_projections", [])) != 4:
    raise SystemExit("MISSING_OBJECT := four_preserved_target_projections")

for forbidden in [
    '"full_native_map_input_contract_discharged": true',
    '"unconditional_non_factorization_theorem_proved": true',
    "unconditional full native-map input contract",
    "NON_FACTORISATION_PROVED",
]:
    if forbidden in json.dumps(artifact, sort_keys=True) or forbidden in doc:
        raise SystemExit("BOUNDARY := forbidden_unconditional_closure_claim")

print("R1_NATIVE_MAP_CONDITIONAL_CONTRACT_CONSTRUCTOR_STATUS_OK")
