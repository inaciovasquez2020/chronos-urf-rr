#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "lean/Chronos/Frontier/RemainingThreeBridgesRouteScan.lean"
artifact = ROOT / "artifacts/chronos/remaining_three_bridges_route_scan_2026_05_24.json"
status = ROOT / "docs/status/REMAINING_THREE_BRIDGES_ROUTE_SCAN_2026_05_24.md"

lean_text = lean.read_text()
status_text = status.read_text()
data = json.loads(artifact.read_text())

for token in [
    "def R2RemainingBridgeRoute",
    "def R3RemainingBridgeRoute",
    "def NonFactorisationRemainingBridgeRoute",
    "theorem unrestricted_r2_naive_promotion_route_refuted",
    "theorem unrestricted_r3_naive_promotion_route_refuted",
    "theorem unrestricted_non_factorisation_naive_promotion_route_refuted",
    "theorem all_remaining_unrestricted_naive_routes_refuted",
    "theorem no_remaining_bridge_theorem_target_closed",
    "remainingRouteRefutationCount : Nat := 3",
    "remainingTheoremTargetClosureCount : Nat := 0",
]:
    assert token in lean_text, token

assert data["status"] == "REMAINING_THREE_UNRESTRICTED_NAIVE_ROUTES_REFUTED_THEOREM_TARGETS_OPEN"
assert data["remaining_route_refutation_count"] == 3
assert data["remaining_theorem_target_closure_count"] == 0
assert len(data["closed_route_refutations"]) == 3
assert len(data["still_open"]) == 3

for token in [
    "DiameterSeparationFillingObstructionProofTarget",
    "UniformLocalTypeCapacityProofTarget",
    "NonFactorisationBridgeProofTarget",
    "LongChordExclusionProofTarget",
    "FourBridgesSourceSolved theorem closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in status_text, token
    assert token in data["does_not_prove"] or token in data["still_open"], token

print("remaining three bridges route scan verifier OK")
