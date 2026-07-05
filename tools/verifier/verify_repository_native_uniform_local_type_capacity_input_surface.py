#!/usr/bin/env python3
from pathlib import Path

lean_path = Path("lean/Chronos/Frontier/R1R2R3IsolatedTargetsConditionalClosure.lean")
text = lean_path.read_text()

required = [
    "structure RepositoryNativeUniformLocalTypeCapacityConfiguration where",
    "localTypeCapacity : Nat",
    "def RepositoryNativeUniformLocalTypeCapacityConfiguration.LocalType",
    "Fin C.localTypeCapacity",
    "def repositoryNativeUniformLocalTypeCapacityBound : Nat",
    "theorem RepositoryNativeUniformLocalTypeCapacityConfiguration.bounded",
    "def repositoryNativeUniformLocalTypeCapacityInputSurface",
    "theorem repository_native_UniformLocalTypeCapacityInputSurface_instance",
    "Nonempty UniformLocalTypeCapacityInputSurface",
    "Configuration := RepositoryNativeUniformLocalTypeCapacityConfiguration",
    "LocalType := RepositoryNativeUniformLocalTypeCapacityConfiguration.LocalType",
    "CapacityBound := repositoryNativeUniformLocalTypeCapacityBound",
    "bounded := RepositoryNativeUniformLocalTypeCapacityConfiguration.bounded",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit(f"missing repository-native uniform local-type capacity witness: {missing[0]}")

forbidden = [
    "theorem repository_native_R1R2R3_geometric_closure",
    "def repositoryNativeR1R2R3GeometricClosure",
    "theorem unrestricted_R1_R2_R3_geometric_closure",
    "def unrestrictedR1R2R3GeometricClosure",
]

present = [needle for needle in forbidden if needle in text]
if present:
    raise SystemExit(f"forbidden unrestricted R1/R2/R3 promotion detected: {present[0]}")

print("REPOSITORY_NATIVE_UNIFORM_LOCAL_TYPE_CAPACITY_INPUT_SURFACE_OK")
