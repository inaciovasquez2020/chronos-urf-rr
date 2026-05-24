#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
lean = root / "lean/Chronos/Frontier/FourBridgesSourceSolvedOpenTarget.lean"
artifact = root / "artifacts/chronos/four_bridges_source_solved_open_target_2026_05_24.json"
status = root / "docs/status/FOUR_BRIDGES_SOURCE_SOLVED_OPEN_TARGET_2026_05_24.md"

lean_text = lean.read_text()
status_text = status.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure FourBridgesSourceSolved",
    "def FourBridgesSourceSolvedOpenTarget",
    "def solve_R1_bridge_theorem_stub",
    "def solve_R2_bridge_theorem_stub",
    "def solve_R3_bridge_theorem_stub",
    "def solve_NON_FACTORISATION_bridge_theorem_stub",
    "def r1_counterexample_search_harness",
    "def r2_counterexample_search_harness",
    "def r3_counterexample_search_harness",
    "def non_factorisation_counterexample_search_harness",
    "theorem unrestricted_r1_native_promotion_refuted_first",
    "theorem exactly_one_bridge_first_result_is_closed",
    "closedFirstBridgeResultCount : Nat := 1",
]

for token in required_lean:
    assert token in lean_text, token

assert data["status"] == "FOUR_BRIDGES_SOURCE_SOLVED_OPEN_TARGET_ONLY"
assert data["open_target"] == "FourBridgesSourceSolved"
assert len(data["bridge_stubs"]) == 4
assert len(data["counterexample_search_harnesses"]) == 4
assert data["closed_first_bridge_result"]["bridge"] == "R1"
assert data["closed_first_bridge_result"]["closed_result_count"] == 1

required_boundaries = [
    "LongChordExclusionProofTarget",
    "DiameterSeparationFillingObstructionProofTarget",
    "UniformLocalTypeCapacityProofTarget",
    "NonFactorisationBridgeProofTarget",
    "NON_FACTORISATION",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for token in required_boundaries:
    assert token in status_text, token
    assert token in data["does_not_prove"], token

print("four bridges source solved open target verifier OK")
