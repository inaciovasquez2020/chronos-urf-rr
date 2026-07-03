#!/usr/bin/env python3
from pathlib import Path

path = Path("lean/Chronos/Frontier/R1R2R3IsolatedTargetsConditionalClosure.lean")
text = path.read_text()

forbidden = "def NonFactorisationProofTarget : Prop := True"
required = [
    "structure NonFactorisationInputSurface where",
    "Object : Type",
    "Factorisation : Object → Prop",
    "admissible_object : Object",
    "non_factorisation : ¬ Factorisation admissible_object",
    "def NonFactorisationProofTarget : Prop :=\n  Nonempty NonFactorisationInputSurface",
]

if forbidden in text:
    raise SystemExit("NON_FACTORISATION_INPUT_SURFACE_REJECTED_TRUE_PLACEHOLDER")

missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"MISSING_OBJECT := {missing[0]}")

print("NON_FACTORISATION_INPUT_SURFACE_OK")
