from pathlib import Path

path = Path("lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContractFromTargets.lean")
if not path.exists():
    raise SystemExit("MISSING_OBJECT := lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContractFromTargets.lean")

text = path.read_text()

required = [
    "structure R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets",
    "longChord : R1LongChordExclusionDischargeTarget D",
    "diameter : R1DiameterSeparationFillingObstructionDischargeTarget",
    "uniform : R1UniformLocalTypeCapacityDischargeTarget",
    "compatibility : R1SourceToNativeCompatibilityDischargeTarget",
    "diameterSourceMatchesLongChord : diameter.source = longChord.source",
    "uniformSourceMatchesLongChord : uniform.source = longChord.source",
    "compatibilitySourceMatchesLongChord : compatibility.source = longChord.source",
    "def r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets",
    "R1ConcreteNewsteinFGLToNativeMapInputContract D where",
    "longChordExclusionEvidence := x.longChord.longChordExclusionEvidence",
    "diameterSeparationFillingObstructionEvidence :=",
    "uniformLocalTypeCapacityEvidence := x.uniform.uniformLocalTypeCapacityEvidence",
    "sourceToNativeCompatibilityEvidence :=",
    "r1_native_map_input_contract_from_aligned_targets_long_chord_eq",
    "r1_native_map_input_contract_from_aligned_targets_diameter_eq",
    "r1_native_map_input_contract_from_aligned_targets_uniform_eq",
    "r1_native_map_input_contract_from_aligned_targets_compatibility_eq",
]

missing = [token for token in required if token not in text]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

for forbidden in [
    "axiom ",
    "opaque ",
    "sorry",
    "admit",
    "NON_FACTORISATION_PROVED",
    "r1_concrete_newstein_fgl_to_native_map_input_contract_closed",
]:
    if forbidden in text:
        raise SystemExit("BOUNDARY := forbidden_unconditional_or_unsound_claim")

print("R1_NATIVE_MAP_INPUT_CONTRACT_CONDITIONAL_CONSTRUCTOR_FROM_TARGETS_OK")
