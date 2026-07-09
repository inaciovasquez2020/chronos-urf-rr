#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "artifacts/status/r1_newstein_fgl_native_non_alias_data_r1_theorem_route_receipt_2026_07_09.json"

required_added_targets = {
    "R1ConcreteNewsteinFGLNativeNonAliasData",
    "R1ConcreteNewsteinFGLNativeNonAliasDataToR1aInputFieldTarget",
    "R1ConcreteNewsteinFGLNativeNonAliasDataToR1bInputFieldTarget",
    "R1ConcreteNewsteinFGLNativeNonAliasDataToR1cInputFieldTarget",
    "R1ConcreteNewsteinFGLNativeNonAliasDataR1InputAssemblyTarget",
    "R1ConcreteNewsteinFGLNativeNonAliasDataR1InputAssemblyTarget.toR1LongChordExclusionTheorem",
}

required_non_claims = {
    "does not prove native non-alias evidence from repository geometry",
    "does not discharge R1ConcreteNewsteinFGLToNativeMapInputContract",
    "does not prove R1TheoremProofInputs from native data alone",
    "does not prove unrestricted R1",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove any Clay problem",
}

data = json.loads(RECEIPT.read_text())

assert data["id"] == "r1_newstein_fgl_native_non_alias_data_r1_theorem_route_receipt_2026_07_09"
assert data["scope"] == "bounded native non-alias data R1 theorem route"
assert set(data["added_targets"]) == required_added_targets
assert required_non_claims.issubset(set(data["non_claims"]))
assert data["remaining_boundary"] == "BOUNDARY := ¬ repository_native_non_alias_Newstein_FGL_geometry_constructs_full_R1TheoremProofInputs"

for commit in data["commits"]:
    assert isinstance(commit, str)
    assert len(commit) >= 7

print("R1_NEWSTEIN_FGL_NATIVE_NON_ALIAS_DATA_R1_THEOREM_ROUTE_RECEIPT_OK")
