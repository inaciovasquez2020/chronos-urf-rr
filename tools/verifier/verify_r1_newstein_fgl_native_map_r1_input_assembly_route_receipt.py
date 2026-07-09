#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "artifacts/status/r1_newstein_fgl_native_map_r1_input_assembly_route_receipt_2026_07_09.json"

required_added_targets = {
    "R1ConcreteNewsteinFGLToNativeMapR1aInputFieldTarget",
    "R1ConcreteNewsteinFGLToNativeMapR1bInputFieldTarget",
    "R1ConcreteNewsteinFGLToNativeMapR1cInputFieldTarget",
    "R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget",
    "R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget.toR1TheoremProofInputsExists",
    "R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget.toR1LongChordExclusionTheorem",
}

required_non_claims = {
    "does not construct repository-native non-alias Newstein/FGL geometry",
    "does not discharge R1ConcreteNewsteinFGLToNativeMapInputContract",
    "does not prove full R1TheoremProofInputs from native data alone",
    "does not prove unrestricted R1",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove any Clay problem",
}

data = json.loads(RECEIPT.read_text())

assert data["id"] == "r1_newstein_fgl_native_map_r1_input_assembly_route_receipt_2026_07_09"
assert data["scope"] == "bounded R1 native-map input assembly route"
assert set(data["added_targets"]) == required_added_targets
assert required_non_claims.issubset(set(data["non_claims"]))
assert data["remaining_boundary"] == "BOUNDARY := ¬ repository_native_non_alias_Newstein_FGL_geometry_constructs_full_R1TheoremProofInputs"

for commit in data["commits"]:
    assert isinstance(commit, str)
    assert len(commit) >= 7

print("R1_NEWSTEIN_FGL_NATIVE_MAP_R1_INPUT_ASSEMBLY_ROUTE_RECEIPT_OK")
