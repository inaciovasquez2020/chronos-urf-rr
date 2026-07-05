#!/usr/bin/env python3
from pathlib import Path

lean_path = Path("lean/Chronos/Frontier/ConcreteNativeR3SemanticData.lean")
text = lean_path.read_text()

required = [
    "structure RepositoryNativeR3IsolatedSemanticSurface where",
    "data : R3SemanticData",
    "theoremClosed : R3UniformLocalTypeCapacityTheorem data",
    "def repositoryNativeR3IsolatedSemanticSurface",
    "data := concreteNativeR3SemanticData",
    "theoremClosed := concrete_native_r3_correct",
    "theorem repository_native_R3_isolated_targets_input_surface",
    "Nonempty RepositoryNativeR3IsolatedSemanticSurface",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit(f"missing repository-native R3 isolated semantic surface: {missing[0]}")

forbidden = [
    "theorem repository_native_R1R2R3_geometric_closure",
    "def repositoryNativeR1R2R3GeometricClosure",
    "theorem unrestricted_R1_R2_R3_geometric_closure",
    "def unrestrictedR1R2R3GeometricClosure",
]

present = [needle for needle in forbidden if needle in text]
if present:
    raise SystemExit(f"forbidden unrestricted R1/R2/R3 promotion detected: {present[0]}")

print("REPOSITORY_NATIVE_R3_ISOLATED_SEMANTIC_SURFACE_OK")
