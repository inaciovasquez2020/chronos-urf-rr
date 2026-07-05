#!/usr/bin/env python3
from pathlib import Path

lean_path = Path("lean/Chronos/Frontier/ConcreteNativeR1SemanticData.lean")
text = lean_path.read_text()

required = [
    "structure RepositoryNativeR1IsolatedSemanticSurface where",
    "data : R1SemanticData",
    "theoremClosed : R1LongChordExclusionTheorem data",
    "def repositoryNativeR1IsolatedSemanticSurface",
    "data := concreteNativeR1SemanticData",
    "theoremClosed := concrete_native_r1_correct",
    "theorem repository_native_R1_isolated_targets_input_surface",
    "Nonempty RepositoryNativeR1IsolatedSemanticSurface",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit(f"missing repository-native R1 isolated semantic surface: {missing[0]}")

forbidden = [
    "theorem repository_native_R1R2R3_geometric_closure",
    "def repositoryNativeR1R2R3GeometricClosure",
    "theorem unrestricted_R1_R2_R3_geometric_closure",
    "def unrestrictedR1R2R3GeometricClosure",
]

present = [needle for needle in forbidden if needle in text]
if present:
    raise SystemExit(f"forbidden unrestricted R1/R2/R3 promotion detected: {present[0]}")

print("REPOSITORY_NATIVE_R1_ISOLATED_SEMANTIC_SURFACE_OK")
