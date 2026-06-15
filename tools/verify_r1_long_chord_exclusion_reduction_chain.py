#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/r1_long_chord_exclusion_reduction_chain_2026_06_15.json"

FORBIDDEN = (
    "unconditional theorem closure",
    "R1 solved",
    "R1 theorem solved",
    "FGL solved",
    "scientific closure achieved",
)

REQUIRED_COMPONENTS = {"R1a", "R1b", "R1c"}

data = json.loads(ARTIFACT.read_text())

assert data["artifact"] == "R1_LONG_CHORD_EXCLUSION_REDUCTION_CHAIN"
assert data["status"] == "conditional_reduction_chain"
assert data["target"]["formal_shape"] == "∀ i ∈ {1,2}, ∀ w ∈ W^triv, e_i ∉ supp(w)"
assert data["boundary"] == "BOUNDARY := ¬ R1_solved"

component_ids = {c["id"] for c in data["components"]}
assert component_ids == REQUIRED_COMPONENTS

for component in data["components"]:
    assert component["required_for_r1"] is True
    assert (ROOT / component["artifact"]).exists(), component["artifact"]
    assert (ROOT / component["verifier"]).exists(), component["verifier"]

does_not_claim = set(data["combination_rule"]["does_not_claim"])
assert "unconditional R1 theorem closure" in does_not_claim
assert "full FGL closure" in does_not_claim
assert "scientific closure" in does_not_claim

text = ARTIFACT.read_text()
for phrase in FORBIDDEN:
    assert phrase not in text, phrase

assert "repo-native formal bridge" in data["weakest_remaining_missing_object"]

print("R1_LONG_CHORD_EXCLUSION_REDUCTION_CHAIN_OK")
