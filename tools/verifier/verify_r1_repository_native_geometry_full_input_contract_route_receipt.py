#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "artifacts/status/r1_repository_native_geometry_full_input_contract_route_receipt_2026_07_09.json"

required_added_targets = {
    "R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractTarget",
    "R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractTarget.toRepositoryNativeGeometryR1Route",
    "R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractR1RouteTarget",
    "R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractTarget.toR1LongChordExclusionTheorem",
}

required_non_claims = {
    "does not prove repository-native geometry evidence",
    "does not prove native non-alias evidence",
    "does not discharge R1ConcreteNewsteinFGLToNativeMapInputContract",
    "does not prove unrestricted R1",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove any Clay problem",
}

data = json.loads(RECEIPT.read_text())

assert data["id"] == "r1_repository_native_geometry_full_input_contract_route_receipt_2026_07_09"
assert data["scope"] == "bounded repository-native geometry full input contract route"
assert set(data["added_targets"]) == required_added_targets
assert required_non_claims.issubset(set(data["non_claims"]))
assert data["remaining_boundary"] == "BOUNDARY := ¬ repository_native_non_alias_Newstein_FGL_geometry_constructs_full_R1TheoremProofInputs"

for commit in data["commits"]:
    assert isinstance(commit, str)
    assert len(commit) >= 7

print("R1_REPOSITORY_NATIVE_GEOMETRY_FULL_INPUT_CONTRACT_ROUTE_RECEIPT_OK")
