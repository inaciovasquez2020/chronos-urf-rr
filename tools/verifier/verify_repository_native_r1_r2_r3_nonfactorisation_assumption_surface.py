#!/usr/bin/env python3
from pathlib import Path
import re

path = Path("lean/Chronos/Frontier/R1R2R3AxiomBoundaryClosure.lean")
text = path.read_text()

required = [
    "def RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumption : Prop :=",
    "RepositoryNativeR1R2R3InstanceTarget → NonFactorisationProofTarget",
    "structure RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumptionSurface where",
    "bridge : RepositoryNativeR1R2R3InstanceTarget → NonFactorisationProofTarget",
    "def RepositoryNativeR1R2R3ConditionalNonFactorisationFromBridgeAssumption",
    "(_S : RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumptionSurface) : Prop :=",
    "theorem repository_native_R1_R2_R3_conditional_nonfactorisation_from_bridge_assumption",
    "(S : RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumptionSurface) :",
    "S.bridge",
]

for needle in required:
    if needle not in text:
        raise SystemExit(f"missing repository-native nonfactorisation assumption surface object: {needle}")

forbidden = [
    "theorem repository_native_R1_R2_R3_unconditional_nonfactorisation",
    "theorem repository_native_R1_R2_R3_nonfactorisation :",
    "def repository_native_R1_R2_R3_unconditional_nonfactorisation",
    "def repository_native_R1_R2_R3_nonfactorisation :",
    "RepositoryNativeR1R2R3UnconditionalNonFactorisation",
]

for needle in forbidden:
    if needle in text:
        raise SystemExit(f"forbidden unconditional nonfactorisation detected: {needle}")

bad_unconditional = re.search(
    r"theorem\s+(?!NonFactorisationProofTarget_conditional_on_surface)"
    r"\w*[Nn]on[Ff]actorisation\w*\s*:\s*NonFactorisationProofTarget\s*:=",
    text,
)
if bad_unconditional:
    raise SystemExit(
        "forbidden theorem proving unconditional NonFactorisationProofTarget detected: "
        + bad_unconditional.group(0).split(":=", 1)[0].strip()
    )

missing_object_boundary_required = [
    "MISSING_OBJECT := inhabitant_of_RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumptionSurface",
    "def repository_native_R1_R2_R3_to_nonfactorisation_bridge_assumption_surface_inhabitant_missing_object : Prop :=",
    "Nonempty RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumptionSurface",
]

for needle in missing_object_boundary_required:
    if needle not in text:
        raise SystemExit(f"missing bridge assumption inhabitant boundary token: {needle}")

forbidden_surface_inhabitant = re.search(
    r"(?m)^\s*(def|theorem|example)\s+"
    r"(?!repository_native_R1_R2_R3_to_nonfactorisation_bridge_assumption_surface_inhabitant_missing_object\b)"
    r"[A-Za-z0-9_'.]*[\s\S]{0,300}?:\s*"
    r"(Nonempty\s+)?RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumptionSurface\s*:=",
    text,
)
if forbidden_surface_inhabitant:
    raise SystemExit(
        "forbidden bridge assumption surface inhabitant detected: "
        + forbidden_surface_inhabitant.group(0).split(":=", 1)[0].strip()
    )

forbidden_inhabited_instance = re.search(
    r"(?m)^\s*instance\s+[A-Za-z0-9_'.]*[\s\S]{0,300}?:\s*"
    r"Inhabited\s+RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumptionSurface\s*:=",
    text,
)
if forbidden_inhabited_instance:
    raise SystemExit(
        "forbidden bridge assumption surface Inhabited instance detected: "
        + forbidden_inhabited_instance.group(0).split(":=", 1)[0].strip()
    )

print("REPOSITORY_NATIVE_R1_R2_R3_NONFACTORISATION_ASSUMPTION_SURFACE_OK")
