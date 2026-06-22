import json
from pathlib import Path

artifact_path = Path("artifacts/chronos/r1_source_to_native_compatibility_evidence_shape_missing_inhabitant_boundary_2026_06_22.json")
doc_path = Path("docs/status/R1_SOURCE_TO_NATIVE_COMPATIBILITY_EVIDENCE_SHAPE_MISSING_INHABITANT_BOUNDARY.md")
lean_path = Path("lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean")
shape_verifier = Path("tools/verify_r1_source_to_native_compatibility_evidence_shape.py")
bridge_verifier = Path("tools/verify_r1_source_to_native_compatibility_invariant_target_bridge.py")

for path in [artifact_path, doc_path, lean_path, shape_verifier, bridge_verifier]:
    if not path.exists():
        raise SystemExit(f"MISSING_OBJECT := {path}")

artifact = json.loads(artifact_path.read_text())
doc = doc_path.read_text()
lean = lean_path.read_text()
shape_verifier_text = shape_verifier.read_text()
bridge_verifier_text = bridge_verifier.read_text()

required_artifact = {
    "status": "R1_SOURCE_TO_NATIVE_COMPATIBILITY_EVIDENCE_SHAPE_MISSING_INHABITANT_BOUNDARY",
    "input_head": "63f2aa95",
    "evidence_shape": "R1SourceToNativeCompatibilityEvidenceShape",
    "invariant_shape": "R1SourceToNativeCompatibilityInvariantShape",
    "target": "r1_source_to_native_compatibility_invariant_shape_target",
    "conditional_discharge_bridge": "r1_source_to_native_compatibility_discharge_target_from_evidence_shape",
    "missing_object": "inhabitant_of_R1SourceToNativeCompatibilityEvidenceShape",
    "supplies_evidence": False,
    "full_native_map_input_contract_discharged": False,
    "unconditional_non_factorization_theorem_proved": False,
}

for key, expected in required_artifact.items():
    if artifact.get(key) != expected:
        raise SystemExit(f"MISSING_OBJECT := artifact.{key}")

required_tokens = [
    "R1SourceToNativeCompatibilityEvidenceShape",
    "R1SourceToNativeCompatibilityInvariantShape",
    "r1_source_to_native_compatibility_invariant_shape_target",
    "r1_source_to_native_compatibility_discharge_target_from_evidence_shape",
    "r1_source_to_native_compatibility_from_evidence_shape_target_eq",
    "inhabitant_of_R1SourceToNativeCompatibilityEvidenceShape",
    "The evidence shape is named, but no inhabitant is supplied.",
    "This status does not prove source-to-native compatibility evidence.",
    "This status does not discharge the full native-map input contract.",
    "This status does not prove the unconditional non-factorization theorem.",
    "R1_SOURCE_TO_NATIVE_COMPATIBILITY_EVIDENCE_SHAPE_OK",
    "R1_SOURCE_TO_NATIVE_COMPATIBILITY_INVARIANT_TARGET_BRIDGE_OK",
]

haystack = "\n".join([
    json.dumps(artifact, sort_keys=True),
    doc,
    lean,
    shape_verifier_text,
    bridge_verifier_text,
])

missing = [token for token in required_tokens if token not in haystack]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

for forbidden in [
    '"supplies_evidence": true',
    '"full_native_map_input_contract_discharged": true',
    '"unconditional_non_factorization_theorem_proved": true',
    "NON_FACTORISATION_PROVED",
    "inhabitant supplied",
]:
    if forbidden in json.dumps(artifact, sort_keys=True) or forbidden in doc:
        raise SystemExit("BOUNDARY := forbidden_evidence_or_closure_claim")

print("R1_SOURCE_TO_NATIVE_COMPATIBILITY_EVIDENCE_SHAPE_MISSING_INHABITANT_BOUNDARY_OK")
