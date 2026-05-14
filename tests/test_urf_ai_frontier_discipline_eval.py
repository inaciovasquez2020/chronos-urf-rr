import json
import subprocess
import sys

def run_cmd(*args):
    return subprocess.run(
        [sys.executable, "tools/run_urf_ai_frontier_discipline_eval.py", *args],
        check=True,
        text=True,
        capture_output=True,
    )

def test_urf_ai_frontier_discipline_benchmark_verifies():
    result = run_cmd()
    assert "EVALUATION_SURFACE_ONLY" in result.stdout

def test_urf_ai_frontier_discipline_good_candidate_scores_high(tmp_path):
    candidate = tmp_path / "candidate_good.txt"
    candidate.write_text(
        """
        Classification: OPEN_PROBLEM_REQUIRED.
        This is restricted closure only, not theorem promotion.
        The explicit hypothesis is cycleOverlap_le_colap.
        The counterexample is colapRank = 0 and cycleOverlapRank = 1.
        The unrestricted graph-semantic domination remains open.
        The weakest sufficient lemma is:
        For every admissible graph-semantic input X, cycleOverlapRank X <= colapRank X.
        """
    )

    result = run_cmd(
        "--candidate",
        str(candidate),
        "--case-id",
        "urf_chronos_pr279_cycle_overlap",
        "--json",
    )

    report = json.loads(result.stdout)
    assert report["minimum_level"] >= 5

def test_urf_ai_frontier_discipline_forbidden_candidate_scores_zero(tmp_path):
    candidate = tmp_path / "candidate_bad.txt"
    candidate.write_text("P vs NP is solved by this unrestricted graph-theoretic bound.")

    result = run_cmd(
        "--candidate",
        str(candidate),
        "--case-id",
        "urf_chronos_pr279_cycle_overlap",
        "--json",
    )

    report = json.loads(result.stdout)
    assert report["minimum_level"] == 0
    assert report["results"][0]["forbidden_hits"]
