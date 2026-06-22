import json
from pathlib import Path

artifact_path = Path("artifacts/chronos/r1_native_map_remaining_evidence_obligation_rank_2026_06_22.json")
doc_path = Path("docs/status/R1_NATIVE_MAP_REMAINING_EVIDENCE_OBLIGATION_RANK.md")
decomposition_path = Path("artifacts/chronos/r1_native_map_input_contract_decomposition_status_2026_06_22.json")

required_paths = [
    artifact_path,
    doc_path,
    decomposition_path,
    Path("lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean"),
    Path("lean/Chronos/Frontier/R1DiameterSeparationFillingObstructionDischargeTarget.lean"),
    Path("lean/Chronos/Frontier/R1UniformLocalTypeCapacityDischargeTarget.lean"),
    Path("tools/verify_r1_source_to_native_compatibility_invariant_shape.py"),
    Path("tools/verify_r1_source_to_native_compatibility_evidence_shape.py"),
]

for path in required_paths:
    if not path.exists():
        raise SystemExit(f"MISSING_OBJECT := {path}")

artifact = json.loads(artifact_path.read_text())
decomposition = json.loads(decomposition_path.read_text())
doc = doc_path.read_text()

if artifact.get("status") != "R1_NATIVE_MAP_REMAINING_EVIDENCE_OBLIGATION_RANK":
    raise SystemExit("MISSING_OBJECT := status")
if artifact.get("input_head") != "a1b631db":
    raise SystemExit("MISSING_OBJECT := input_head_a1b631db")
if artifact.get("full_native_map_input_contract_discharged") is not False:
    raise SystemExit("BOUNDARY := unexpected_full_contract_discharge")
if artifact.get("unconditional_non_factorization_theorem_proved") is not False:
    raise SystemExit("BOUNDARY := unexpected_unconditional_non_factorization_theorem")

ranked = artifact.get("ranked_remaining_evidence_obligations", [])
if len(ranked) != 3:
    raise SystemExit("MISSING_OBJECT := three_ranked_remaining_evidence_obligations")

expected = [
    (
        1,
        "r1SourceToNativeCompatibility",
        "R1SourceToNativeCompatibilityDischargeTarget",
        "sourceToNativeCompatibilityEvidence",
    ),
    (
        2,
        "r1DiameterSeparationFillingObstruction",
        "R1DiameterSeparationFillingObstructionDischargeTarget",
        "diameterSeparationFillingObstructionEvidence",
    ),
    (
        3,
        "r1UniformLocalTypeCapacity",
        "R1UniformLocalTypeCapacityDischargeTarget",
        "uniformLocalTypeCapacityEvidence",
    ),
]

for item, (rank, field, target, evidence) in zip(ranked, expected):
    if item.get("rank") != rank:
        raise SystemExit(f"MISSING_OBJECT := rank_{rank}")
    if item.get("field") != field:
        raise SystemExit(f"MISSING_OBJECT := {field}")
    if item.get("target_interface") != target:
        raise SystemExit(f"MISSING_OBJECT := {target}")
    if item.get("missing_evidence") != evidence:
        raise SystemExit(f"MISSING_OBJECT := {evidence}")

source_item = ranked[0]
if source_item.get("status") != "evidence_shape_present_missing_inhabitant":
    raise SystemExit("MISSING_OBJECT := source_compatibility_evidence_shape_status")
if source_item.get("invariant_shape") != "R1SourceToNativeCompatibilityInvariantShape":
    raise SystemExit("MISSING_OBJECT := R1SourceToNativeCompatibilityInvariantShape")
if source_item.get("invariant_target") != "r1_source_to_native_compatibility_invariant_shape_target":
    raise SystemExit("MISSING_OBJECT := r1_source_to_native_compatibility_invariant_shape_target")
if source_item.get("evidence_shape") != "R1SourceToNativeCompatibilityEvidenceShape":
    raise SystemExit("MISSING_OBJECT := R1SourceToNativeCompatibilityEvidenceShape")
if source_item.get("conditional_discharge_bridge") != "r1_source_to_native_compatibility_discharge_target_from_evidence_shape":
    raise SystemExit("MISSING_OBJECT := r1_source_to_native_compatibility_discharge_target_from_evidence_shape")
if source_item.get("target_projection") != "r1_source_to_native_compatibility_from_evidence_shape_target_eq":
    raise SystemExit("MISSING_OBJECT := r1_source_to_native_compatibility_from_evidence_shape_target_eq")

decomposition_statuses = {
    field["field"]: field["status"]
    for field in decomposition.get("native_map_input_contract_fields", [])
}
for _, field, _, _ in expected:
    if decomposition_statuses.get(field) != "discharge_target_interface_present_missing_evidence":
        raise SystemExit(f"MISSING_OBJECT := decomposition_status_for_{field}")

required_doc_tokens = [
    "The full native-map input contract is not discharged.",
    "The unconditional non-factorization theorem is not proved.",
    "sourceToNativeCompatibilityEvidence",
    "R1SourceToNativeCompatibilityInvariantShape",
    "r1_source_to_native_compatibility_invariant_shape_target",
    "R1SourceToNativeCompatibilityEvidenceShape",
    "r1_source_to_native_compatibility_discharge_target_from_evidence_shape",
    "r1_source_to_native_compatibility_from_evidence_shape_target_eq",
    "diameterSeparationFillingObstructionEvidence",
    "uniformLocalTypeCapacityEvidence",
    "Introduce a missing-inhabitant boundary lock",
]

missing_doc = [token for token in required_doc_tokens if token not in doc]
if missing_doc:
    raise SystemExit("MISSING_OBJECT := " + missing_doc[0])

for forbidden in [
    '"full_native_map_input_contract_discharged": true',
    '"unconditional_non_factorization_theorem_proved": true',
    "supplies missing evidence",
    "NON_FACTORISATION_PROVED",
]:
    if forbidden in json.dumps(artifact, sort_keys=True) or forbidden in doc:
        raise SystemExit("BOUNDARY := forbidden_closure_claim")

print("R1_NATIVE_MAP_REMAINING_EVIDENCE_OBLIGATION_RANK_OK")
