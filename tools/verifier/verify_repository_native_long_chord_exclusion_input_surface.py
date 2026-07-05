#!/usr/bin/env python3
from pathlib import Path

lean_path = Path("lean/Chronos/Frontier/R1R2R3IsolatedTargetsConditionalClosure.lean")
text = lean_path.read_text()

required = [
    "structure RepositoryNativeLongChordConfiguration where",
    "endpointSeparation : Nat",
    "admissibleDiameter : Nat",
    "def RepositoryNativeLongChordConfiguration.LongChord",
    "def RepositoryNativeLongChordConfiguration.Admissible",
    "theorem RepositoryNativeLongChordConfiguration.exclusion",
    "def repositoryNativeLongChordExclusionInputSurface",
    "theorem repository_native_LongChordExclusionInputSurface_instance",
    "Nonempty LongChordExclusionInputSurface",
    "Configuration := RepositoryNativeLongChordConfiguration",
    "LongChord := RepositoryNativeLongChordConfiguration.LongChord",
    "Admissible := RepositoryNativeLongChordConfiguration.Admissible",
    "exclusion := RepositoryNativeLongChordConfiguration.exclusion",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit(f"missing repository-native long-chord surface witness: {missing[0]}")

forbidden = [
    "theorem repository_native_R1R2R3_geometric_closure",
    "def repositoryNativeR1R2R3GeometricClosure",
    "theorem unrestricted_R1_R2_R3_geometric_closure",
    "def unrestrictedR1R2R3GeometricClosure",
]

present = [needle for needle in forbidden if needle in text]
if present:
    raise SystemExit(f"forbidden unrestricted R1/R2/R3 promotion detected: {present[0]}")

print("REPOSITORY_NATIVE_LONG_CHORD_EXCLUSION_INPUT_SURFACE_OK")
