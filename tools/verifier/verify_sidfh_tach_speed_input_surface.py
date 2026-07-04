#!/usr/bin/env python3
from pathlib import Path
import sys

path = Path("lean/Chronos/Frontier/SIDFHTachSpeedInputSurface.lean")
text = path.read_text()

required = [
    "structure SIDFHTachSpeedInputSurface where",
    "properTimeRate : State → ℝ",
    "slower_moves_faster_in_time",
    "Nonempty SIDFHTachSpeedInputSurface",
    "sidfhTachSpeedUniversalPhysicalClosureBoundary",
]

for needle in required:
    if needle not in text:
        print(f"MISSING_OBJECT := {needle}")
        sys.exit(1)

for forbidden in [
    "SIDFHTachSpeedInputSurface : Prop := True",
    "SIDFHTachSpeedProofTarget : Prop := True",
    "axiom ",
    "opaque ",
    "sorry",
    "admit",
]:
    if forbidden in text:
        print(f"FORBIDDEN_OBJECT := {forbidden}")
        sys.exit(1)

print("SIDFH_TACH_SPEED_INPUT_SURFACE_OK")
