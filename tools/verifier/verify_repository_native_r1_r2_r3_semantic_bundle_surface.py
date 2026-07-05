#!/usr/bin/env python3
from pathlib import Path

lean_path = Path("lean/Chronos/Frontier/ConcreteNativeBindingSpec.lean")
text = lean_path.read_text()

required = [
    "structure RepositoryNativeR1R2R3SemanticBundleSurface where",
    "r1Closed : R1LongChordExclusionTheorem concreteNativeR1SemanticData",
    "r2Closed : R2DiameterSeparationFillingObstructionTheorem concreteNativeR2SemanticData",
    "r3Closed : R3UniformLocalTypeCapacityTheorem concreteNativeR3SemanticData",
    "def repositoryNativeR1R2R3SemanticBundleSurface",
    "r1Closed := concrete_native_r1_correct",
    "r2Closed := concrete_native_r2_correct",
    "r3Closed := concrete_native_r3_correct",
    "def RepositoryNativeR1R2R3SemanticBundleTheoremClosure",
    "theorem repository_native_R1_R2_R3_semantic_bundle_theorem_closure",
    "theorem repository_native_R1_R2_R3_semantic_bundle_surface",
    "Nonempty RepositoryNativeR1R2R3SemanticBundleSurface",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit(f"missing repository-native R1/R2/R3 semantic bundle surface: {missing[0]}")

forbidden = [
    "theorem repository_native_R1R2R3_geometric_closure",
    "def repositoryNativeR1R2R3GeometricClosure",
    "theorem unrestricted_R1_R2_R3_geometric_closure",
    "def unrestrictedR1R2R3GeometricClosure",
]

present = [needle for needle in forbidden if needle in text]
if present:
    raise SystemExit(f"forbidden unrestricted R1/R2/R3 promotion detected: {present[0]}")

print("REPOSITORY_NATIVE_R1_R2_R3_SEMANTIC_BUNDLE_SURFACE_OK")
