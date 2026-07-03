#!/usr/bin/env python3
from pathlib import Path

path = Path("lean/Chronos/Frontier/R1R2R3IsolatedTargetsConditionalClosure.lean")
text = path.read_text()

forbidden = "def DiameterSeparationFillingObstructionProofTarget : Prop := True"
required = [
    "structure DiameterSeparationFillingObstructionInputSurface where",
    "Configuration : Type",
    "DiameterSeparated : Configuration → Prop",
    "Fillable : Configuration → Prop",
    "obstruction : ∀ C, DiameterSeparated C → ¬ Fillable C",
    "def DiameterSeparationFillingObstructionProofTarget : Prop :=\n  Nonempty DiameterSeparationFillingObstructionInputSurface",
]

if forbidden in text:
    raise SystemExit("DIAMETER_SEPARATION_FILLING_OBSTRUCTION_INPUT_SURFACE_REJECTED_TRUE_PLACEHOLDER")

missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"MISSING_OBJECT := {missing[0]}")

print("DIAMETER_SEPARATION_FILLING_OBSTRUCTION_INPUT_SURFACE_OK")
