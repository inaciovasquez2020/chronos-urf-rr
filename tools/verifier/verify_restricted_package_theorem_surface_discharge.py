#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "Chronos" / "Frontier" / "H4_1_FGL_FinalSelectedInputClosure.lean"

text = TARGET.read_text(encoding="utf-8")

required_fragments = [
    "def restricted_package_theorem_surface_closed : Prop :=",
    "∀ I : H4_1_FGL_FinalSelectedInput.{u, v},",
    "∃ C : H4_1_FGL_FinalSelectedInputClosure.{u, v},",
    "C.input = I",
    "theorem selected_observation_layer_to_named_restricted_package_surface :",
    "restricted_package_theorem_surface_closed := by",
    "exact ⟨H4_1_FGL_FinalSelectedInputClosure.ofInput I, rfl⟩",
]

for fragment in required_fragments:
    if fragment not in text:
        raise SystemExit(f"missing restricted package theorem surface discharge fragment: {fragment}")

for forbidden in ["sorry", "admit", "axiom ", "opaque "]:
    if forbidden in text:
        raise SystemExit(f"forbidden Lean placeholder found in {TARGET}: {forbidden}")

print("RESTRICTED_PACKAGE_THEOREM_SURFACE_DISCHARGE_OK")
