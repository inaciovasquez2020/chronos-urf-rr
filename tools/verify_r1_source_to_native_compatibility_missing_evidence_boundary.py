from pathlib import Path

contract_path = Path("lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContract.lean")
contract = contract_path.read_text()
frontier = "\n".join(path.read_text() for path in Path("lean/Chronos/Frontier").glob("*.lean"))

required_contract = [
    "structure R1ConcreteNewsteinFGLToNativeMapInputContract",
    "r1SourceToNativeCompatibility : Prop",
    "sourceToNativeCompatibilityEvidence : r1SourceToNativeCompatibility",
]

missing = [token for token in required_contract if token not in contract]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

forbidden_evidence_names = [
    "r1_concrete_newstein_fgl_source_to_native_compatibility_evidence",
    "r1_concrete_newstein_fgl_source_to_native_compatibility_discharge_target",
    "r1_concrete_newstein_fgl_to_native_map_source_compatibility_evidence",
    "r1_concrete_newstein_fgl_to_native_map_source_compatibility_discharge_target",
]

present_forbidden = [token for token in forbidden_evidence_names if token in frontier]
if present_forbidden:
    raise SystemExit("BOUNDARY := unexpected_existing_source_to_native_compatibility_bridge_" + present_forbidden[0])

print("R1_SOURCE_TO_NATIVE_COMPATIBILITY_MISSING_EVIDENCE_BOUNDARY_OK")
