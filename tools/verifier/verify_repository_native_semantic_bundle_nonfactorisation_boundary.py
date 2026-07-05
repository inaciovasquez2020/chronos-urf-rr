#!/usr/bin/env python3
from pathlib import Path
import re

bundle_path = Path("lean/Chronos/Frontier/ConcreteNativeBindingSpec.lean")
bridge_path = Path("lean/Chronos/Frontier/R1R2R3AxiomBoundaryClosure.lean")

bundle = bundle_path.read_text()
bridge = bridge_path.read_text()

required_bundle = [
    "import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure",
    "def RepositoryNativeSemanticBundleToNonFactorisationMissingObject : Prop :=",
    "RepositoryNativeR1R2R3SemanticBundleTheoremClosure",
    "repositoryNativeR1R2R3SemanticBundleSurface",
    "NonFactorisationProofTarget",
    "def repository_native_semantic_bundle_to_nonfactorisation_boundary : String :=",
    "MISSING_OBJECT := repository_native_semantic_bundle_to_nonfactorisation_bridge",
    "theorem repository_native_semantic_bundle_does_not_supply_nonfactorisation_bridge",
]

required_bridge = [
    "def RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumption : Prop :=",
    "RepositoryNativeR1R2R3InstanceTarget → NonFactorisationProofTarget",
]

for needle in required_bundle:
    if needle not in bundle:
        raise SystemExit(f"missing semantic-bundle-to-nonfactorisation boundary object: {needle}")

for needle in required_bridge:
    if needle not in bridge:
        raise SystemExit(f"missing located repository-native nonfactorisation bridge target: {needle}")

forbidden_substrings = [
    "theorem repository_native_semantic_bundle_to_nonfactorisation",
    "def repository_native_semantic_bundle_to_nonfactorisation_bridge",
    "theorem repository_native_R1_R2_R3_semantic_bundle_nonfactorisation",
    "theorem unrestricted_R1_R2_R3_geometric_closure",
    "def unrestricted_R1_R2_R3_geometric_closure",
    "def unrestrictedR1R2R3GeometricClosure",
    "theorem unrestrictedR1R2R3GeometricClosure",
]

for needle in forbidden_substrings:
    if needle in bundle:
        raise SystemExit(f"forbidden semantic-bundle promotion detected: {needle}")

bad_direct = re.search(
    r"theorem\s+\w*(?:[Ss]emantic[Bb]undle)\w*(?:[Nn]on[Ff]actorisation)\w*"
    r"\s*:[^:=]*NonFactorisationProofTarget\s*:=",
    bundle,
    flags=re.S,
)
if bad_direct:
    raise SystemExit("forbidden direct theorem from semantic bundle to NonFactorisationProofTarget detected")

print("REPOSITORY_NATIVE_SEMANTIC_BUNDLE_NONFACTORISATION_BOUNDARY_OK")
