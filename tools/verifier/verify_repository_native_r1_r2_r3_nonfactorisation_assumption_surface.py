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

decl_start = re.compile(
    r"(?m)^\s*(def|theorem|example|instance)\s+([A-Za-z0-9_'.]+)\b"
)
decls = list(decl_start.finditer(text))
for index, decl in enumerate(decls):
    kind = decl.group(1)
    name = decl.group(2)
    next_start = decls[index + 1].start() if index + 1 < len(decls) else len(text)
    header = text[decl.start():next_start].split(":=", 1)[0]

    if name == "repository_native_R1_R2_R3_to_nonfactorisation_bridge_assumption_surface_inhabitant_missing_object":
        continue

    if ":" not in header:
        continue

    result_type = header.rsplit(":", 1)[1].strip()

    if kind in {"def", "theorem", "example"}:
        if re.fullmatch(
            r"(Nonempty\s+)?RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumptionSurface",
            result_type,
        ):
            raise SystemExit(
                "forbidden bridge assumption surface inhabitant detected: "
                + name
            )

    if kind == "instance":
        if re.fullmatch(
            r"Inhabited\s+RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumptionSurface",
            result_type,
        ):
            raise SystemExit(
                "forbidden bridge assumption surface Inhabited instance detected: "
                + name
            )

print("REPOSITORY_NATIVE_R1_R2_R3_NONFACTORISATION_ASSUMPTION_SURFACE_OK")
