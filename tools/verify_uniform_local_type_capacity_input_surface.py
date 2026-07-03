#!/usr/bin/env python3
from pathlib import Path

path = Path("lean/Chronos/Frontier/R1R2R3IsolatedTargetsConditionalClosure.lean")
text = path.read_text()

forbidden = "def UniformLocalTypeCapacityProofTarget : Prop := True"
required = [
    "structure UniformLocalTypeCapacityInputSurface where",
    "Configuration : Type",
    "LocalType : Configuration → Type",
    "CapacityBound : Nat",
    "bounded : ∀ C, Nonempty (LocalType C) → CapacityBound ≥ 0",
    "def UniformLocalTypeCapacityProofTarget : Prop :=\n  Nonempty UniformLocalTypeCapacityInputSurface",
]

if forbidden in text:
    raise SystemExit("UNIFORM_LOCAL_TYPE_CAPACITY_INPUT_SURFACE_REJECTED_TRUE_PLACEHOLDER")

missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"MISSING_OBJECT := {missing[0]}")

print("UNIFORM_LOCAL_TYPE_CAPACITY_INPUT_SURFACE_OK")
