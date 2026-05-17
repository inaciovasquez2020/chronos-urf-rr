#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import py_compile
import sys

ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs/status/RATE_THICK_BINARY_KAPPA_EMPIRICAL_MODEL_2026_05_17.md"
ART = ROOT / "artifacts/chronos/rate_thick_binary_kappa_empirical_model_2026_05_17.json"
EXP = ROOT / "experiments/rate_thick_binary_kappa_empirical"

REQUIRED_FILES = [
    EXP / "urf_empirical_model.py",
    EXP / "holdout_compare.py",
    EXP / "loocv_ratio_stability.py",
    EXP / "ratio_stability_slack_compare.py",
    EXP / "sample_data.csv",
]

REQUIRED_DOC_PHRASES = [
    "EMPIRICAL_MODEL_ONLY / NO_THEOREM_PROMOTION",
    "Train-minimum kappa domination failed on holdout.",
    "Observed maximum slack required: `0.016941176470588237`.",
    "Empirical comparison only.",
    "Does not prove:",
    "entropy-minimum domination",
    "ratio stability",
    "uniform fiber-mass bound",
    "unrestricted RateThickFiberCoercivity",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

FORBIDDEN_DOC_PHRASES = [
    "proves entropy-minimum domination",
    "proves ratio stability",
    "proves uniform fiber-mass bound",
    "proves unrestricted RateThickFiberCoercivity",
    "proves unrestricted UniversalFiberEntropyGap",
    "proves Chronos-RR",
    "proves H4.1/FGL",
    "proves P vs NP",
    "proves any Clay problem",
    "theorem_promotion\": true",
]


def read_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with (EXP / "sample_data.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            lam = float(row["lambda"])
            entropy_mass = float(row["entropy_mass"])
            rank_rate = float(row["rank_rate"])
            kappa = lam * (1.0 - lam)
            ratio = entropy_mass / kappa
            rows.append({
                "lambda": lam,
                "entropy_mass": entropy_mass,
                "rank_rate": rank_rate,
                "split": row["split"],
                "kappa": kappa,
                "ratio": ratio,
                "theory_admissible": 0.0 < lam <= 0.5,
                "rank_positive": rank_rate > 0.0,
            })
    return rows


def assert_close(actual: float, expected: float, tol: float = 1e-12) -> None:
    assert abs(actual - expected) <= tol, (actual, expected)


def main() -> None:
    for path in REQUIRED_FILES:
        assert path.exists(), path

    for path in REQUIRED_FILES:
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)

    doc = DOC.read_text()
    for phrase in REQUIRED_DOC_PHRASES:
        assert phrase in doc, phrase
    for phrase in FORBIDDEN_DOC_PHRASES:
        assert phrase not in doc, phrase

    data = json.loads(ART.read_text())
    assert data["status"] == "EMPIRICAL_MODEL_ONLY"
    assert data["theorem_promotion"] is False
    assert_close(data["delta_observed_max"], 0.016941176470588237)
    assert data["train_min_domination_failures"] == 2
    assert data["loocv_train_min_domination_failures"] == 1
    assert data["holdout_safe_domination_failures"] == 0
    assert data["uniform_bound_failures"] == 0

    rows = [
        r for r in read_rows()
        if r["theory_admissible"] and r["rank_positive"] and r["kappa"] > 0.0
    ]
    train = [r for r in rows if r["split"] == "train"]
    test = [r for r in rows if r["split"] == "test"]

    assert len(rows) == 8
    assert len(train) == 4
    assert len(test) == 4

    alpha_train_min = min(float(r["ratio"]) for r in train)
    alpha_holdout_safe = min(float(r["ratio"]) for r in test)
    delta_holdout = alpha_train_min - alpha_holdout_safe
    epsilon_train_min = min(float(r["entropy_mass"]) for r in train)

    train_min_failures = sum(
        1 for r in test
        if float(r["entropy_mass"]) - alpha_train_min * float(r["kappa"]) < 0.0
    )
    holdout_safe_failures = sum(
        1 for r in test
        if float(r["entropy_mass"]) - alpha_holdout_safe * float(r["kappa"]) < -1e-12
    )
    uniform_failures = sum(
        1 for r in test
        if float(r["entropy_mass"]) < epsilon_train_min
    )

    loocv_slacks = []
    for i, holdout in enumerate(rows):
        train_rows = [r for j, r in enumerate(rows) if i != j]
        alpha = min(float(r["ratio"]) for r in train_rows)
        loocv_slacks.append(max(0.0, alpha - float(holdout["ratio"])))

    assert_close(alpha_train_min, 1.0196078431372548)
    assert_close(alpha_holdout_safe, 1.0026666666666666)
    assert_close(delta_holdout, 0.016941176470588237)
    assert_close(max(loocv_slacks), 0.016380952380952385)
    assert_close(epsilon_train_min, 0.05)
    assert train_min_failures == 2
    assert holdout_safe_failures == 0
    assert uniform_failures == 0

    print("Rate-thick binary kappa empirical model verified.")


if __name__ == "__main__":
    main()
