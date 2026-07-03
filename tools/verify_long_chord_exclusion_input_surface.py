#!/usr/bin/env python3
from pathlib import Path

path = Path("lean/Chronos/Frontier/R1R2R3IsolatedTargetsConditionalClosure.lean")
text = path.read_text()

forbidden = "def LongChordExclusionProofTarget : Prop := True"
required = [
    "structure LongChordExclusionInputSurface where",
    "Configuration : Type",
    "LongChord : Configuration → Prop",
    "Admissible : Configuration → Prop",
    "exclusion : ∀ C, Admissible C → ¬ LongChord C",
    "def LongChordExclusionProofTarget : Prop :=\n  Nonempty LongChordExclusionInputSurface",
]

if forbidden in text:
    raise SystemExit("LONG_CHORD_EXCLUSION_INPUT_SURFACE_REJECTED_TRUE_PLACEHOLDER")

missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"MISSING_OBJECT := {missing[0]}")

print("LONG_CHORD_EXCLUSION_INPUT_SURFACE_OK")
