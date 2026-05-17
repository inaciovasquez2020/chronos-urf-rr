#!/usr/bin/env python3
import json
from pathlib import Path

import pandas as pd


def main() -> None:
    df = pd.read_csv("sample_data.csv")
    df["kappa"] = df["lambda"] * (1 - df["lambda"])
    df["admissible_theory"] = (df["lambda"] > 0) & (df["lambda"] <= 0.5)
    df["rank_positive"] = df["rank_rate"] > 0
    df["ratio"] = df["entropy_mass"] / df["kappa"]

    base = df[
        df["admissible_theory"]
        & df["rank_positive"]
        & (df["kappa"] > 0)
    ].copy().reset_index(drop=True)

    rows = []
    for i in range(len(base)):
        holdout = base.iloc[i]
        train = base.drop(index=i)

        alpha_train_min = float(train["ratio"].min())
        alpha_holdout = float(holdout["ratio"])
        slack_required = max(0.0, alpha_train_min - alpha_holdout)
        relative_slack_required = (
            slack_required / alpha_train_min if alpha_train_min > 0 else None
        )

        rows.append({
            "holdout_lambda": float(holdout["lambda"]),
            "holdout_entropy_mass": float(holdout["entropy_mass"]),
            "holdout_kappa": float(holdout["kappa"]),
            "holdout_ratio": alpha_holdout,
            "alpha_train_min": alpha_train_min,
            "slack_required": slack_required,
            "relative_slack_required": relative_slack_required,
            "train_min_domination_pass": slack_required == 0.0,
        })

    out = pd.DataFrame(rows)

    report = {
        "rows": int(len(out)),
        "train_min_domination_failures": int((~out["train_min_domination_pass"]).sum()),
        "max_slack_required": float(out["slack_required"].max()),
        "max_relative_slack_required": float(out["relative_slack_required"].max()),
        "holdout_safe_alpha_global": float(base["ratio"].min()),
        "status": {
            "ratio_stability": "empirical_slack_estimated",
            "train_min_kappa_domination": "rejected_if_failures_positive",
            "unrestricted_theorem_closure": "not_claimed",
        },
    }

    Path("out_loocv").mkdir(exist_ok=True)
    out.to_csv("out_loocv/loocv_ratio_stability.csv", index=False)
    Path("out_loocv/loocv_ratio_stability_report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )

    print(json.dumps(report, indent=2))
    print()
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
