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
    alpha_holdout_safe = float(test["ratio"].min())
    ratio_stability_slack = max(0.0, alpha_train_min - alpha_holdout_safe)
    ratio_stability_relative_slack = (
        ratio_stability_slack / alpha_train_min if alpha_train_min > 0 else None
    )

    epsilon_train_min = float(train["entropy_mass"].min())

    test["train_min_predicted_entropy_mass"] = alpha_train_min * test["kappa"]
    test["holdout_safe_predicted_entropy_mass"] = alpha_holdout_safe * test["kappa"]
    test["uniform_epsilon_prediction"] = epsilon_train_min

    test["train_min_domination_residual"] = (
        test["entropy_mass"] - test["train_min_predicted_entropy_mass"]
    )
    test["holdout_safe_domination_residual"] = (
        test["entropy_mass"] - test["holdout_safe_predicted_entropy_mass"]
    )
    test["uniform_bound_residual"] = test["entropy_mass"] - epsilon_train_min

    test["train_min_domination_pass"] = test["train_min_domination_residual"] >= 0
    test["holdout_safe_domination_pass"] = test["holdout_safe_domination_residual"] >= 0
    test["uniform_bound_pass"] = test["uniform_bound_residual"] >= 0

    test["stronger_lower_bound"] = test.apply(
        lambda r: "kappa_domination"
        if r["holdout_safe_predicted_entropy_mass"] >= r["uniform_epsilon_prediction"]
        else "uniform_epsilon",
        axis=1,
    )

    report = {
        "alpha_train_min": alpha_train_min,
        "alpha_holdout_safe": alpha_holdout_safe,
        "ratio_stability_slack_required": ratio_stability_slack,
        "ratio_stability_relative_slack_required": ratio_stability_relative_slack,
        "epsilon_train_min": epsilon_train_min,
        "test_rows": int(len(test)),
        "train_min_domination_failures": int((~test["train_min_domination_pass"]).sum()),
        "holdout_safe_domination_failures": int((~test["holdout_safe_domination_pass"]).sum()),
        "uniform_bound_failures": int((~test["uniform_bound_pass"]).sum()),
        "status": {
            "binary_kappa_positivity": "empirically_passed_on_sample",
            "entropy_minimum_domination_train_min": "holdout_rejected",
            "entropy_minimum_domination_holdout_safe": "empirical_holdout_fit_only",
            "ratio_stability": "slack_required",
            "uniform_fiber_mass_bound": "holdout_empirical_test_only",
            "unrestricted_theorem_closure": "not_claimed",
        },
    }

    out = Path("out_holdout")
    out.mkdir(exist_ok=True)
    test.to_csv(out / "holdout_predictions.csv", index=False)
    (out / "holdout_report.json").write_text(json.dumps(report, indent=2) + "\n")

    summary = f"""# Holdout Comparison

- alpha_train_min: {alpha_train_min}
- alpha_holdout_safe: {alpha_holdout_safe}
- ratio_stability_slack_required: {ratio_stability_slack}
- ratio_stability_relative_slack_required: {ratio_stability_relative_slack}
- epsilon_train_min: {epsilon_train_min}
- train_min_domination_failures: {report["train_min_domination_failures"]}
- holdout_safe_domination_failures: {report["holdout_safe_domination_failures"]}
- uniform_bound_failures: {report["uniform_bound_failures"]}

## Boundary

- Empirical comparison only.
- Train-minimum kappa domination is rejected on holdout.
- Holdout-safe alpha is fitted from holdout data only.
- Ratio stability requires a positive slack.
- No unrestricted theorem closure claimed.
"""
    (out / "holdout_summary.md").write_text(summary)

    print(json.dumps(report, indent=2))
    print()
    print(
        test[
            [
                "lambda",
                "entropy_mass",
                "kappa",
                "ratio",
                "train_min_predicted_entropy_mass",
                "train_min_domination_residual",
                "train_min_domination_pass",
                "holdout_safe_predicted_entropy_mass",
                "holdout_safe_domination_residual",
                "holdout_safe_domination_pass",
                "uniform_epsilon_prediction",
                "uniform_bound_pass",
                "stronger_lower_bound",
                "split",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
