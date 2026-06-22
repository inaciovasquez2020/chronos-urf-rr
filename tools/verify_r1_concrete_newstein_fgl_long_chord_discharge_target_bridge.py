from pathlib import Path

lean = Path("lean/Chronos/Frontier/R1LongChordExclusionDischargeTarget.lean").read_text()

required = [
    "def r1_concrete_newstein_fgl_source_long_chord_discharge_target",
    "R1LongChordExclusionDischargeTarget R1ConcreteNativeSafeSemanticData",
    "R1LongChordExclusionTheorem R1ConcreteNativeSafeSemanticData",
    "r1_concrete_native_safe_long_chord_exclusion_from_concrete_newstein_fgl_source x",
]

missing = [token for token in required if token not in lean]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

print("R1_CONCRETE_NEWSTEIN_FGL_LONG_CHORD_DISCHARGE_TARGET_BRIDGE_OK")
