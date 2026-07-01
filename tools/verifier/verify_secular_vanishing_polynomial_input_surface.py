#!/usr/bin/env python3
from pathlib import Path

lean_path = Path("lean/Chronos/Frontier/SecularVanishingPolynomialInputSurface.lean")
old_path = Path("lean/Chronos/Frontier/SecularPolynomialVanishingInputSurface.lean")

if old_path.exists():
    raise SystemExit(f"FORBIDDEN_OBJECT := {old_path}")

text = lean_path.read_text()

required = [
    "structure SecularVanishingPolynomial",
    "polynomial : α → Int",
    "secularVanishes : ∀ x : α, polynomial x = 0",
    "def SecularVanishingPolynomialInputSurface",
    "Nonempty (SecularVanishingPolynomial α)",
    "structure SecularVanishingPolynomialSource",
    "sourceForcesSecularVanishes : ∀ x : α, polynomial x = 0",
    "def SecularVanishingPolynomialSourceSurface",
    "theorem secularVanishingPolynomialSource_to_inputSurface",
    "theorem secularVanishingPolynomialInputSurface_zeroWitness",
    "BOUNDARY := secular vanishing polynomial is primitive input structure; not antisymmetry, not involution, not cancellation",
]

for needle in required:
    if needle not in text:
        raise SystemExit(f"MISSING_OBJECT := {needle}")

forbidden_substitution_symbols = [
    "SecularPolynomialAntisymmetryInput",
    "SecularInvolutionInput",
    "SecularWeakOrbitVanishing",
    "secularPolynomialAntisymmetry_to_weakOrbitVanishing",
    "iota_iota",
    "antisymmetric :",
]

for needle in forbidden_substitution_symbols:
    if needle in text:
        raise SystemExit(f"FORBIDDEN_SUBSTITUTION := {needle}")

print("SECULAR_VANISHING_POLYNOMIAL_INPUT_SURFACE_OK")
