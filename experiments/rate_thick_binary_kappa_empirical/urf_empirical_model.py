#!/usr/bin/env python3
"""
URF empirical comparison model.

Input CSV columns:

required:
  lambda
  entropy_mass

optional:
  rank_rate
  fiber_count
  admissible
  split

Theory:

  admissible(lambda) := 0 < lambda <= 1/2

  kappa(lambda) := lambda * (1 - lambda)

  BinaryKappaPositivity:
      admissible(lambda) -> kappa(lambda) > 0

  EntropyMinimumDomination(alpha):
      entropy_mass >= alpha * kappa(lambda)

  UniformFiberMassBound(epsilon):
      admissible(lambda) and rank_rate > 0 -> entropy_mass >= epsilon

Empirical estimators:

  alpha_hat(q) := quantile_q(entropy_mass / kappa(lambda))
  epsilon_hat := min entropy_mass over admissible rank-positive rows

Comparison outputs:

  model_report.json
  model_predictions.csv
  model_summary.md
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {"lambda", "entropy_mass"}


def kappa(lam: np.ndarray) -> np.ndarray:
    return lam * (1.0 - lam)


def admissible(lam: np.ndarray) -> np.ndarray:
    return (lam > 0.0) & (lam <= 0.5)


def bootstrap_quantile_ci(
    values: np.ndarray,
    q: float,
    n_boot: int,
    seed: int,
) -> dict[str, float]:
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return {"lo": math.nan, "mid": math.nan, "hi": math.nan}

    rng = np.random.default_rng(seed)
    boots = []
    n = len(values)

    for _ in range(n_boot):
        sample = values[rng.integers(0, n, size=n)]
        boots.append(float(np.quantile(sample, q)))

    return {
        "lo": float(np.quantile(boots, 0.025)),
        "mid": float(np.quantile(boots, 0.5)),
        "hi": float(np.quantile(boots, 0.975)),
    }


def bootstrap_min_ci(
    values: np.ndarray,
    n_boot: int,
    seed: int,
) -> dict[str, float]:
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return {"lo": math.nan, "mid": math.nan, "hi": math.nan}

    rng = np.random.default_rng(seed)
    boots = []
    n = len(values)

    for _ in range(n_boot):
        sample = values[rng.integers(0, n, size=n)]
        boots.append(float(np.min(sample)))

    return {
        "lo": float(np.quantile(boots, 0.025)),
        "mid": float(np.quantile(boots, 0.5)),
        "hi": float(np.quantile(boots, 0.975)),
    }


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise SystemExit(f"missing required columns: {sorted(missing)}")

    df = df.copy()
    df["lambda"] = pd.to_numeric(df["lambda"], errors="coerce")
    df["entropy_mass"] = pd.to_numeric(df["entropy_mass"], errors="coerce")

    if "rank_rate" not in df.columns:
        df["rank_rate"] = 1.0
    else:
        df["rank_rate"] = pd.to_numeric(df["rank_rate"], errors="coerce").fillna(0.0)

    if "fiber_count" not in df.columns:
        df["fiber_count"] = 1.0
    else:
        df["fiber_count"] = pd.to_numeric(df["fiber_count"], errors="coerce").fillna(1.0)

    if "admissible" not in df.columns:
        df["admissible"] = admissible(df["lambda"].to_numpy())
    else:
        df["admissible"] = df["admissible"].astype(str).str.lower().isin(
            {"1", "true", "yes", "y"}
        )

    if "split" not in df.columns:
        df["split"] = "all"

    df = df.dropna(subset=["lambda", "entropy_mass"]).reset_index(drop=True)
    return df


def evaluate(df: pd.DataFrame, q: float, n_boot: int, seed: int) -> tuple[pd.DataFrame, dict[str, Any]]:
    out = df.copy()

    lam = out["lambda"].to_numpy(dtype=float)
    mass = out["entropy_mass"].to_numpy(dtype=float)
    rank_rate = out["rank_rate"].to_numpy(dtype=float)
    is_adm = out["admissible"].to_numpy(dtype=bool)

    out["kappa"] = kappa(lam)
    out["theory_admissible"] = admissible(lam)
    out["binary_kappa_positive"] = out["theory_admissible"] & (out["kappa"] > 0.0)
    out["rank_positive"] = rank_rate > 0.0

    valid = is_adm & np.isfinite(mass) & np.isfinite(out["kappa"].to_numpy()) & (out["kappa"].to_numpy() > 0.0)
    ratios = mass[valid] / out.loc[valid, "kappa"].to_numpy(dtype=float)

    alpha_hat = float(np.quantile(ratios, q)) if len(ratios) else math.nan
    alpha_ci = bootstrap_quantile_ci(ratios, q, n_boot, seed)

    out["predicted_entropy_mass"] = alpha_hat * out["kappa"]
    out["domination_residual"] = out["entropy_mass"] - out["predicted_entropy_mass"]
    out["domination_pass"] = out["domination_residual"] >= 0.0

    uniform_mask = valid & (rank_rate > 0.0)
    uniform_values = mass[uniform_mask]
    epsilon_hat = float(np.min(uniform_values)) if len(uniform_values) else math.nan
    epsilon_ci = bootstrap_min_ci(uniform_values, n_boot, seed + 1)

    out["uniform_bound_prediction"] = epsilon_hat
    out["uniform_bound_pass"] = out["entropy_mass"] >= epsilon_hat

    report = {
        "n_rows": int(len(out)),
        "n_admissible": int(np.sum(is_adm)),
        "n_theory_admissible": int(np.sum(out["theory_admissible"])),
        "n_rank_positive_admissible": int(np.sum(uniform_mask)),
        "binary_kappa_positive_failures": int(np.sum(out["theory_admissible"] & ~(out["kappa"] > 0.0))),
        "alpha_quantile": q,
        "alpha_hat": alpha_hat,
        "alpha_bootstrap_ci": alpha_ci,
        "epsilon_hat": epsilon_hat,
        "epsilon_bootstrap_ci": epsilon_ci,
        "domination_failure_count": int(np.sum(valid & ~out["domination_pass"].to_numpy(dtype=bool))),
        "domination_failure_rate": float(np.mean(~out.loc[valid, "domination_pass"])) if np.sum(valid) else math.nan,
        "uniform_bound_failure_count": int(np.sum(uniform_mask & ~out["uniform_bound_pass"].to_numpy(dtype=bool))),
        "uniform_bound_failure_rate": float(np.mean(~out.loc[uniform_mask, "uniform_bound_pass"])) if np.sum(uniform_mask) else math.nan,
        "status": {
            "binary_kappa_positivity": "empirically_passed" if int(np.sum(out["theory_admissible"] & ~(out["kappa"] > 0.0))) == 0 else "empirically_failed",
            "entropy_minimum_domination": "empirical_fit_only",
            "uniform_fiber_mass_bound": "empirical_fit_only",
            "unrestricted_theorem_closure": "not_claimed",
        },
    }

    return out, report


def write_summary(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# URF Empirical Model Summary",
        "",
        f"- rows: {report['n_rows']}",
        f"- admissible rows: {report['n_admissible']}",
        f"- theory-admissible rows: {report['n_theory_admissible']}",
        f"- rank-positive admissible rows: {report['n_rank_positive_admissible']}",
        f"- binary kappa positivity failures: {report['binary_kappa_positive_failures']}",
        f"- alpha_hat: {report['alpha_hat']}",
        f"- alpha bootstrap CI: {report['alpha_bootstrap_ci']}",
        f"- epsilon_hat: {report['epsilon_hat']}",
        f"- epsilon bootstrap CI: {report['epsilon_bootstrap_ci']}",
        f"- domination failure count: {report['domination_failure_count']}",
        f"- domination failure rate: {report['domination_failure_rate']}",
        f"- uniform bound failure count: {report['uniform_bound_failure_count']}",
        f"- uniform bound failure rate: {report['uniform_bound_failure_rate']}",
        "",
        "## Boundary",
        "",
        "- Empirical comparison only.",
        "- Does not prove entropy-minimum domination.",
        "- Does not prove uniform fiber-mass bound.",
        "- Does not prove unrestricted RateThickFiberCoercivity.",
        "- Does not prove unrestricted UniversalFiberEntropyGap.",
        "- Does not prove Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.",
        "",
    ]
    path.write_text("\n".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, type=Path)
    ap.add_argument("--outdir", default=Path("out"), type=Path)
    ap.add_argument("--alpha-quantile", default=0.05, type=float)
    ap.add_argument("--bootstrap", default=1000, type=int)
    ap.add_argument("--seed", default=20260517, type=int)
    args = ap.parse_args()

    if not (0.0 <= args.alpha_quantile <= 1.0):
        raise SystemExit("--alpha-quantile must be in [0,1]")

    args.outdir.mkdir(parents=True, exist_ok=True)

    df = load_data(args.data)
    pred, report = evaluate(df, args.alpha_quantile, args.bootstrap, args.seed)

    pred.to_csv(args.outdir / "model_predictions.csv", index=False)
    (args.outdir / "model_report.json").write_text(json.dumps(report, indent=2) + "\n")
    write_summary(args.outdir / "model_summary.md", report)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
