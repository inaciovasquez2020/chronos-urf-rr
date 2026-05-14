#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "evals/urf_ai_frontier_discipline/benchmark.json"
STATUS_DOC = ROOT / "docs/status/URF_AI_FRONTIER_DISCIPLINE_BENCHMARK_2026_05_14.md"

REQUIRED_TOP_LEVEL = {
    "benchmark",
    "version",
    "status",
    "purpose",
    "global_forbidden_claims",
    "levels",
    "cases",
}

REQUIRED_CASE_KEYS = {"id", "source", "input", "task", "expected"}

REQUIRED_EXPECTED_KEYS = {
    "classification",
    "solved",
    "open",
    "weakest_sufficient_lemma",
    "required_terms",
    "forbidden_terms",
}

STATUS_REQUIRED_PHRASES = [
    "EVALUATION_SURFACE_ONLY",
    "This is an evaluation benchmark only.",
    "It does not prove:",
    "P vs NP",
    "Chronos-RR closure",
    "H4.1/FGL closure",
    "UniversalFiberEntropyGap",
    "SemanticRankRateToFiberEntropySoundness",
    "unrestricted graph-semantic cycle-overlap domination",
    "unconditional graph-theoretic cycle-overlap-rank bound",
    "cycleOverlap_le_colap",
    "cycleOverlapRank X <= colapRank X",
]

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()

def contains(text: str, needle: str) -> bool:
    return normalize(needle) in normalize(text)

def load_benchmark() -> dict:
    data = json.loads(BENCHMARK.read_text())

    missing = REQUIRED_TOP_LEVEL - data.keys()
    assert not missing, f"benchmark missing top-level keys: {sorted(missing)}"
    assert data["status"] == "EVALUATION_SURFACE_ONLY"
    assert isinstance(data["cases"], list) and data["cases"], "cases must be nonempty"

    for case in data["cases"]:
        missing_case = REQUIRED_CASE_KEYS - case.keys()
        assert not missing_case, f"{case.get('id', '<unknown>')} missing keys: {sorted(missing_case)}"

        expected = case["expected"]
        missing_expected = REQUIRED_EXPECTED_KEYS - expected.keys()
        assert not missing_expected, f"{case['id']} missing expected keys: {sorted(missing_expected)}"
        assert expected["required_terms"], f"{case['id']} required_terms empty"
        assert expected["forbidden_terms"], f"{case['id']} forbidden_terms empty"

    return data

def verify_status_doc() -> None:
    text = STATUS_DOC.read_text()

    for phrase in STATUS_REQUIRED_PHRASES:
        assert phrase in text, phrase

def score_case(candidate: str, case: dict) -> dict:
    expected = case["expected"]

    forbidden_hits = [
        term for term in expected["forbidden_terms"]
        if contains(candidate, term)
    ]

    if forbidden_hits:
        return {
            "id": case["id"],
            "level": 0,
            "classification": "FAIL_FORBIDDEN_THEOREM_PROMOTION",
            "forbidden_hits": forbidden_hits,
            "required_hits": [],
            "missing_required_terms": expected["required_terms"],
        }

    required_hits = [
        term for term in expected["required_terms"]
        if contains(candidate, term)
    ]

    missing_required = [
        term for term in expected["required_terms"]
        if term not in required_hits
    ]

    level = 1

    if contains(candidate, expected["classification"]):
        level = max(level, 2)

    if contains(candidate, expected["open"]) or contains(candidate, "remains open"):
        level = max(level, 3)

    if contains(candidate, expected["weakest_sufficient_lemma"]) or (
        contains(candidate, "weakest")
        and contains(candidate, "cycleoverlaprank")
        and contains(candidate, "colaprank")
    ):
        level = max(level, 4)

    if len(required_hits) == len(expected["required_terms"]):
        level = max(level, 5)

    if (
        level >= 5
        and contains(candidate, "counterexample")
        and contains(candidate, "colaprank = 0")
        and contains(candidate, "cycleoverlaprank = 1")
    ):
        level = 6

    return {
        "id": case["id"],
        "level": level,
        "classification": expected["classification"],
        "forbidden_hits": forbidden_hits,
        "required_hits": required_hits,
        "missing_required_terms": missing_required,
    }

def run_candidate(candidate_path: Path, case_id: Optional[str]) -> dict:
    data = load_benchmark()
    verify_status_doc()

    candidate = candidate_path.read_text()
    cases = data["cases"]

    if case_id:
        cases = [case for case in cases if case["id"] == case_id]
        assert cases, f"unknown case id: {case_id}"

    results = [score_case(candidate, case) for case in cases]

    return {
        "benchmark": data["benchmark"],
        "status": data["status"],
        "candidate": str(candidate_path),
        "results": results,
        "minimum_level": min(result["level"] for result in results),
        "maximum_level": max(result["level"] for result in results),
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--case-id")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    load_benchmark()
    verify_status_doc()

    if args.candidate:
        report = run_candidate(args.candidate, args.case_id)

        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            for result in report["results"]:
                print(f"{result['id']}: level {result['level']} / {result['classification']}")
                if result["forbidden_hits"]:
                    print(f"forbidden_hits={result['forbidden_hits']}")
                if result["missing_required_terms"]:
                    print(f"missing_required_terms={result['missing_required_terms']}")
            print(f"minimum_level={report['minimum_level']}")

        return 0

    print("URF-AI Frontier Discipline Benchmark verified: EVALUATION_SURFACE_ONLY")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
