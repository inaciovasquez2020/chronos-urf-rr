from pathlib import Path

path = Path("lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean")
if not path.exists():
    raise SystemExit("MISSING_OBJECT := lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean")

text = path.read_text()

required = [
    "structure R1SourceToNativeCompatibilityInvariantShape (D : R1SemanticData) : Type where",
    "def r1_source_to_native_compatibility_invariant_shape_target",
    "structure R1SourceToNativeCompatibilityEvidenceShape (D : R1SemanticData) : Type where",
    "invariant : R1SourceToNativeCompatibilityInvariantShape D",
    "compatibilityEvidence :",
    "r1_source_to_native_compatibility_invariant_shape_target invariant",
    "def r1_source_to_native_compatibility_discharge_target_from_evidence_shape",
    "R1SourceToNativeCompatibilityDischargeTarget where",
    "source := x.invariant.source",
    "r1SourceToNativeCompatibility :=",
    "sourceToNativeCompatibilityEvidence := x.compatibilityEvidence",
    "theorem r1_source_to_native_compatibility_from_evidence_shape_target_eq",
    "rfl",
]

missing = [token for token in required if token not in text]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

shape_start = text.index("structure R1SourceToNativeCompatibilityEvidenceShape")
boundary_start = text.index("def r1_source_to_native_compatibility_discharge_target_boundary")
block = text[shape_start:boundary_start]

for forbidden in [
    "axiom ",
    "opaque ",
    "sorry",
    "admit",
    "NON_FACTORISATION_PROVED",
    "full native-map input contract",
    "r1_concrete_newstein_fgl_to_native_map_input_contract_closed",
]:
    if forbidden in block:
        raise SystemExit("BOUNDARY := forbidden_unconditional_or_unsound_claim")

print("R1_SOURCE_TO_NATIVE_COMPATIBILITY_EVIDENCE_SHAPE_OK")
