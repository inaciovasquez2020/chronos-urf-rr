from pathlib import Path

target = Path("lean/Chronos/Frontier/R1UniformLocalTypeCapacityDischargeTarget.lean").read_text()
frontier = "\n".join(path.read_text() for path in Path("lean/Chronos/Frontier").glob("*.lean"))

required_target = [
    "structure R1UniformLocalTypeCapacityDischargeTarget",
    "source : R1ConcreteNewsteinFGLGeometrySourceObject",
    "r1UniformLocalTypeCapacity : Prop",
    "uniformLocalTypeCapacityEvidence : r1UniformLocalTypeCapacity",
]

missing = [token for token in required_target if token not in target]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

forbidden_bridge_names = [
    "r1_concrete_newstein_fgl_source_uniform_local_type_capacity_discharge_target",
    "r1_concrete_newstein_fgl_source_uniform_local_type_capacity_evidence",
]

present_forbidden = [token for token in forbidden_bridge_names if token in frontier]
if present_forbidden:
    raise SystemExit("BOUNDARY := unexpected_existing_uniform_capacity_bridge_" + present_forbidden[0])

print("R1_UNIFORM_LOCAL_TYPE_CAPACITY_DISCHARGE_TARGET_MISSING_EVIDENCE_BOUNDARY_OK")
