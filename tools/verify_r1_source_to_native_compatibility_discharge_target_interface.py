from pathlib import Path

target_path = Path("lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean")
if not target_path.exists():
    raise SystemExit("MISSING_OBJECT := lean/Chronos/Frontier/R1SourceToNativeCompatibilityDischargeTarget.lean")

target = target_path.read_text()
frontier = "\n".join(path.read_text() for path in Path("lean/Chronos/Frontier").glob("*.lean"))

required = [
    "structure R1SourceToNativeCompatibilityDischargeTarget",
    "source : R1ConcreteNewsteinFGLGeometrySourceObject",
    "r1SourceToNativeCompatibility : Prop",
    "sourceToNativeCompatibilityEvidence : r1SourceToNativeCompatibility",
    "r1_source_to_native_compatibility_discharge_target_boundary",
    "NO_DISCHARGED_R1_SOURCE_TO_NATIVE_COMPATIBILITY_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT",
]

missing = [token for token in required if token not in target]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

forbidden_bridge_names = [
    "r1_concrete_newstein_fgl_source_to_native_compatibility_discharge_target",
    "r1_concrete_newstein_fgl_source_to_native_compatibility_evidence",
]

present_forbidden = [token for token in forbidden_bridge_names if token in frontier]
if present_forbidden:
    raise SystemExit("BOUNDARY := unexpected_existing_source_to_native_compatibility_bridge_" + present_forbidden[0])

print("R1_SOURCE_TO_NATIVE_COMPATIBILITY_DISCHARGE_TARGET_INTERFACE_OK")
