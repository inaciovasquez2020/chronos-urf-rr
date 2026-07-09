#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "artifacts/status/r1_concrete_native_binding_repository_native_geometry_instance_receipt_2026_07_09.json"

required_added_targets = {
    "R1ConcreteNewsteinFGLConcreteNativeBindingToRepositoryNativeGeometryTarget",
    "R1ConcreteNewsteinFGLConcreteNativeBindingToRepositoryNativeGeometryTarget.toRepositoryNativeGeometry",
    "R1ConcreteNewsteinFGLConcreteNativeBindingRepositoryNativeGeometryInstanceInput",
    "R1ConcreteNewsteinFGLConcreteNativeBindingRepositoryNativeGeometryInstanceInput.toRepositoryNativeGeometry",
}

required_non_claims = {
    "does not prove the R1c native interface fields",
    "does not prove native non-alias evidence",
    "does not discharge R1ConcreteNewsteinFGLToNativeMapInputContract",
    "does not prove unrestricted R1",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove any Clay problem",
}

data = json.loads(RECEIPT.read_text())

assert data["id"] == "r1_concrete_native_binding_repository_native_geometry_instance_receipt_2026_07_09"
assert data["scope"] == "bounded concrete native binding repository-native geometry instance input"
assert set(data["added_targets"]) == required_added_targets
assert required_non_claims.issubset(set(data["non_claims"]))
assert data["remaining_boundary"] == "BOUNDARY := ¬ repository_native_non_alias_Newstein_FGL_geometry_constructs_full_R1TheoremProofInputs"

for commit in data["commits"]:
    assert isinstance(commit, str)
    assert len(commit) >= 7

print("R1_CONCRETE_NATIVE_BINDING_REPOSITORY_NATIVE_GEOMETRY_INSTANCE_RECEIPT_OK")
