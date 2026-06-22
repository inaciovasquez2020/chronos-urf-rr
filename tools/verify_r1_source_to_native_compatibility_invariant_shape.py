from pathlib import Path

path = Path("lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean")
if not path.exists():
    raise SystemExit("MISSING_OBJECT := lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean")

text = path.read_text()

required = [
    "structure R1SourceToNativeCompatibilityInvariantShape (D : R1SemanticData) : Type where",
    "source : R1ConcreteNewsteinFGLGeometrySourceObject",
    "sourceToNativeCompatibilityInvariant : Prop",
    "def r1_source_to_native_compatibility_invariant_shape_target",
    "R1SourceToNativeCompatibilityInvariantShape D",
    "x.sourceToNativeCompatibilityInvariant",
    "structure R1SourceToNativeCompatibilityDischargeTarget",
    "sourceToNativeCompatibilityEvidence : r1SourceToNativeCompatibility",
]

missing = [token for token in required if token not in text]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

shape_start = text.index("structure R1SourceToNativeCompatibilityInvariantShape")
target_start = text.index("structure R1SourceToNativeCompatibilityDischargeTarget")
shape_block = text[shape_start:target_start]

for forbidden in [
    "nativeData : R1SemanticData",
    "sourceToNativeCompatibilityEvidence :",
    "compatibilityEvidence :",
    "evidence :",
    "by",
]:
    if forbidden in shape_block:
        raise SystemExit("BOUNDARY := invariant_shape_supplies_evidence_or_reintroduces_universe_field")

print("R1_SOURCE_TO_NATIVE_COMPATIBILITY_INVARIANT_SHAPE_OK")
