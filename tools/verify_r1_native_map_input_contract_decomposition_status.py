import json
from pathlib import Path

ART = Path("artifacts/chronos/r1_native_map_input_contract_decomposition_status_2026_06_22.json")
DOC = Path("docs/status/R1_NATIVE_MAP_INPUT_CONTRACT_DECOMPOSITION_STATUS.md")

source_files = {
    "long_chord_target": Path("lean/Chronos/Frontier/R1LongChordExclusionDischargeTarget.lean"),
    "input_contract": Path("lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContract.lean"),
    "diameter_target": Path("lean/Chronos/Frontier/R1DiameterSeparationFillingObstructionDischargeTarget.lean"),
    "uniform_target": Path("lean/Chronos/Frontier/R1UniformLocalTypeCapacityDischargeTarget.lean"),
    "compatibility_target": Path("lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean"),
}

tool_files = [
    Path("tools/verify_r1_concrete_newstein_fgl_long_chord_discharge_target_bridge.py"),
    Path("tools/verify_r1_concrete_newstein_fgl_to_native_map_long_chord_input_field.py"),
    Path("tools/verify_r1_diameter_separation_discharge_target_missing_evidence_boundary.py"),
    Path("tools/verify_r1_uniform_local_type_capacity_discharge_target_missing_evidence_boundary.py"),
    Path("tools/verify_r1_source_to_native_compatibility_missing_evidence_boundary.py"),
]

for path in [ART, DOC, *source_files.values(), *tool_files]:
    if not path.exists():
        raise SystemExit(f"MISSING_OBJECT := {path}")

artifact = json.loads(ART.read_text())
doc = DOC.read_text()
lean = "\n".join(path.read_text() for path in source_files.values())
tools = "\n".join(path.read_text() for path in tool_files)

required_artifact = {
    "status": "R1_NATIVE_MAP_INPUT_CONTRACT_DECOMPOSITION_STATUS",
    "input_head": "b03a3481",
    "unconditional_non_factorization_theorem_proved": False,
    "full_native_map_input_contract_discharged": False,
    "boundary": "no full native-map input contract; no unconditional non-factorization theorem",
}

for key, expected in required_artifact.items():
    if artifact.get(key) != expected:
        raise SystemExit(f"MISSING_OBJECT := artifact.{key}")

required_tokens = [
    "r1_concrete_newstein_fgl_source_long_chord_discharge_target",
    "r1_concrete_newstein_fgl_to_native_map_input_contract_long_chord_field",
    "R1ConcreteNewsteinFGLToNativeMapInputContract",
    "R1DiameterSeparationFillingObstructionDischargeTarget",
    "R1UniformLocalTypeCapacityDischargeTarget",
    "r1SourceToNativeCompatibility",
    "R1_DIAMETER_SEPARATION_DISCHARGE_TARGET_MISSING_EVIDENCE_BOUNDARY_OK",
    "R1_UNIFORM_LOCAL_TYPE_CAPACITY_DISCHARGE_TARGET_MISSING_EVIDENCE_BOUNDARY_OK",
    "R1_SOURCE_TO_NATIVE_COMPATIBILITY_MISSING_EVIDENCE_BOUNDARY_OK",
    "No full native-map input contract is proved.",
    "No unconditional non-factorization theorem is proved.",
]

haystack = "\n".join([json.dumps(artifact, sort_keys=True), doc, lean, tools])
missing = [token for token in required_tokens if token not in haystack]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

fields = artifact.get("native_map_input_contract_fields", [])
if len(fields) != 4:
    raise SystemExit("MISSING_OBJECT := four_native_map_input_contract_fields")

statuses = {field["field"]: field["status"] for field in fields}
expected_statuses = {
    "r1LongChordExclusion": "wired_evidence_path",
    "r1DiameterSeparationFillingObstruction": "missing_evidence_boundary_locked",
    "r1UniformLocalTypeCapacity": "missing_evidence_boundary_locked",
    "r1SourceToNativeCompatibility": "discharge_target_interface_present_missing_evidence",
}
if statuses != expected_statuses:
    raise SystemExit("MISSING_OBJECT := exact_field_status_partition")

for forbidden in [
    "\"full_native_map_input_contract_discharged\": true",
    "\"unconditional_non_factorization_theorem_proved\": true",
    "NON_FACTORISATION_PROVED",
]:
    if forbidden in json.dumps(artifact, sort_keys=True) or forbidden in doc:
        raise SystemExit("BOUNDARY := forbidden_full_closure_claim")

print("R1_NATIVE_MAP_INPUT_CONTRACT_DECOMPOSITION_STATUS_OK")
