import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_four_bridges_source_solved_open_target_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/four_bridges_source_solved_open_target_2026_05_24.json").read_text()
    )

    assert data["status"] == "FOUR_BRIDGES_SOURCE_SOLVED_OPEN_TARGET_ONLY"
    assert data["open_target"] == "FourBridgesSourceSolved"
    assert len(data["bridge_stubs"]) == 4
    assert len(data["counterexample_search_harnesses"]) == 4
    assert data["closed_first_bridge_result"]["bridge"] == "R1"
    assert data["closed_first_bridge_result"]["closed_result_count"] == 1
    assert "Chronos-RR" in data["does_not_prove"]
    assert "P vs NP" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]


def test_four_bridges_source_solved_open_target_lean_tokens():
    text = (ROOT / "lean/Chronos/Frontier/FourBridgesSourceSolvedOpenTarget.lean").read_text()

    for token in [
        "structure FourBridgesSourceSolved",
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
    ]:
        assert token in text


def test_four_bridges_source_solved_open_target_status_boundaries():
    text = (ROOT / "docs/status/FOUR_BRIDGES_SOURCE_SOLVED_OPEN_TARGET_2026_05_24.md").read_text()

    for token in [
        "FOUR_BRIDGES_SOURCE_SOLVED_OPEN_TARGET_ONLY",
        "RepositoryNativeR1LongChordCoherence",
        "NoRepositoryNativeLongChordWitness",
        "LongChordExclusionProofTarget",
        "DiameterSeparationFillingObstructionProofTarget",
        "UniformLocalTypeCapacityProofTarget",
        "NonFactorisationBridgeProofTarget",
        "NON_FACTORISATION",
        "Chronos-RR",
        "H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert token in text
