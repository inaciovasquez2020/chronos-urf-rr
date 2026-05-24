import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_remaining_three_bridges_route_scan_artifact_counts():
    data = json.loads(
        (ROOT / "artifacts/chronos/remaining_three_bridges_route_scan_2026_05_24.json").read_text()
    )

    assert data["status"] == "REMAINING_THREE_UNRESTRICTED_NAIVE_ROUTES_REFUTED_THEOREM_TARGETS_OPEN"
    assert data["remaining_route_refutation_count"] == 3
    assert data["remaining_theorem_target_closure_count"] == 0
    assert len(data["closed_route_refutations"]) == 3
    assert len(data["still_open"]) == 3


def test_remaining_three_bridges_route_scan_lean_tokens():
    text = (ROOT / "lean/Chronos/Frontier/RemainingThreeBridgesRouteScan.lean").read_text()

    for token in [
        "def R2RemainingBridgeRoute",
        "def R3RemainingBridgeRoute",
        "def NonFactorisationRemainingBridgeRoute",
        "theorem unrestricted_r2_naive_promotion_route_refuted",
        "theorem unrestricted_r3_naive_promotion_route_refuted",
        "theorem unrestricted_non_factorisation_naive_promotion_route_refuted",
        "theorem all_remaining_unrestricted_naive_routes_refuted",
        "theorem no_remaining_bridge_theorem_target_closed",
    ]:
        assert token in text


def test_remaining_three_bridges_route_scan_boundaries():
    text = (ROOT / "docs/status/REMAINING_THREE_BRIDGES_ROUTE_SCAN_2026_05_24.md").read_text()

    for token in [
        "REMAINING_THREE_UNRESTRICTED_NAIVE_ROUTES_REFUTED_THEOREM_TARGETS_OPEN",
        "DiameterSeparationFillingObstructionProofTarget",
        "UniformLocalTypeCapacityProofTarget",
        "NonFactorisationBridgeProofTarget",
        "LongChordExclusionProofTarget",
        "FourBridgesSourceSolved",
        "Chronos-RR",
        "H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert token in text
