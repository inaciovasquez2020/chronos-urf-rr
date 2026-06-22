from pathlib import Path

target = Path("lean/Chronos/Frontier/R1DiameterSeparationFillingObstructionDischargeTarget.lean").read_text()
frontier = "\n".join(path.read_text() for path in Path("lean/Chronos/Frontier").glob("*.lean"))

required_target = [
    "structure R1DiameterSeparationFillingObstructionDischargeTarget",
    "source : R1ConcreteNewsteinFGLGeometrySourceObject",
    "r1DiameterSeparationFillingObstruction : Prop",
    "diameterSeparationFillingObstructionEvidence : r1DiameterSeparationFillingObstruction",
]

missing = [token for token in required_target if token not in target]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

forbidden_bridge_names = [
    "r1_concrete_newstein_fgl_source_diameter_separation_filling_obstruction_discharge_target",
    "r1_concrete_newstein_fgl_source_diameter_separation_filling_obstruction_evidence",
]

present_forbidden = [token for token in forbidden_bridge_names if token in frontier]
if present_forbidden:
    raise SystemExit("BOUNDARY := unexpected_existing_diameter_bridge_" + present_forbidden[0])

print("R1_DIAMETER_SEPARATION_DISCHARGE_TARGET_MISSING_EVIDENCE_BOUNDARY_OK")
