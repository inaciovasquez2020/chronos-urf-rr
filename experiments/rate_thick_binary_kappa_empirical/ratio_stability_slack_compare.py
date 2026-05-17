#!/usr/bin/env python3
import json
from pathlib import Path

import pandas as pd


DELTA_LOOCV = 0.016380952380952385
DELTA_HOLDOUT = 0.016941176470588237
DELTA_OBSERVED_MAX = max(DELTA_LOOCV, DELTA_HOLDOUT)


def main() -> None:
    df = pd.read_csv("sample_data.csv")
    df["kappa"] = df["lambda"] * (1 - df["lambda"])
    df["admissible_theory"] = (df["lambda"] > 0) & (df["lambda"] <= 0.5)
    df["rank_positive"] = df["rank_rate"] > 0
    df["ratio"] = df["entropy_mass"] / df["kappa"]

    train = df[
        (df["split"] == "train")
        & df["admissible_theory"]
        & df["rank_positive"]
        & (df["kappa"] > 0)
    ].copy()

    test = df[
        (df["split"] == "test")
        & df["admissible_theory"]
        & df["rank_positive"]
        & (df["kappa"] > 0)
    ].copy()

    alpha_train_min = float(train["ratio"].min())

    candidates = {
        "no_slack": 0.0,
        "loocv_slack": DELTA_LOOCV,
        "holdout_slack": DELTA_HOLDOUT,
        "observed_max_slack": DELTA_OBSERVED_MAX,
    }

    rows = []
    for name, delta in candidates.items():
        alpha_adjusted = alpha_train_min - delta
        pred = alpha_adjusted * test["kappa"]
        residual = test["entropy_mass"] - pred
        failures = int((residual < 0).sum())

        rows.append({
            "slack_model": name,
            "delta": delta,
            "alpha_train_min": alpha_train_min,
            "alpha_adjusted": alpha_adjusted,
            "test_failures": failures,
            "test_failure_rate": failures / len(test) if len(test) else None,
            "min_test_residual": float(residual.min()) if len(test) else None,
        })

    out = pd.DataFrame(rows)

    report = {
        "alpha_train_min": alpha_train_min,
        "delta_loocv": DELTA_LOOCV,
        "delta_holdout": DELTA_HOLDOUT,
        "delta_observed_max": DELTA_OBSERVED_MAX,
        "passing_slack_models": out.loc[out["test_failures"] == 0, "slack_model"].tolist(),
        "status": {
            "ratio_stability_slack": "empirical_candidate_only",
            "entropy_minimum_domination": "passes_holdout_only_after_slack",
            "unrestricted_theorem_closure": "not_claimed",
        },
    }

    outdir = Path("out_ratio_stability")
    outdir.mkdir(exist_ok=True)
    out.to_csv(outdir / "ratio_stability_slack_compare.csv", index=False)
    (outdir / "ratio_stability_slack_report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )

    print(json.dumps(report, indent=2))
    print()
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
