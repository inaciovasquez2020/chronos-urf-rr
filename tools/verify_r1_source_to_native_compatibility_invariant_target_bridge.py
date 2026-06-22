from pathlib import Path

path = Path("lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean")
if not path.exists():
    raise SystemExit("MISSING_OBJECT := lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean")

text = path.read_text()

required = [
    "structure R1SourceToNativeCompatibilityInvariantShape (D : R1SemanticData) : Type where",
    "def r1_source_to_native_compatibility_invariant_shape_target",
    "structure R1SourceToNativeCompatibilityDischargeTarget",
    "def r1_source_to_native_compatibility_discharge_target_invariant_shape",
    "(D : R1SemanticData)",
    "(x : R1SourceToNativeCompatibilityDischargeTarget)",
    "R1SourceToNativeCompatibilityInvariantShape D where",
    "sourceToNativeCompatibilityInvariant := x.r1SourceToNativeCompatibility",
    "theorem r1_source_to_native_compatibility_discharge_target_invariant_shape_target_eq",
    "r1_source_to_native_compatibility_invariant_shape_target",
    "x.r1SourceToNativeCompatibility := by",
    "rfl",
]

missing = [token for token in required if token not in text]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

bridge_start = text.index("def r1_source_to_native_compatibility_discharge_target_invariant_shape")
boundary_start = text.index("def r1_source_to_native_compatibility_discharge_target_boundary")
bridge_block = text[bridge_start:boundary_start]

for forbidden in [
    "sourceToNativeCompatibilityEvidence :=",
    "compatibilityEvidence :=",
    "exact x.sourceToNativeCompatibilityEvidence",
]:
    if forbidden in bridge_block:
        raise SystemExit("BOUNDARY := bridge_supplies_forbidden_compatibility_evidence")

print("R1_SOURCE_TO_NATIVE_COMPATIBILITY_INVARIANT_TARGET_BRIDGE_OK")
