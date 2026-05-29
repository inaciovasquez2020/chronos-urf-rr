#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "artifacts/sparc/authentic_sparc_theta_residual_prediction_vector_run_2026_05_29.csv"
CSV_OUT = ROOT / "artifacts/sparc/theta_residual_cross_validation_stability_run_2026_05_29.csv"
ART = ROOT / "artifacts/sparc/theta_residual_cross_validation_stability_run_2026_05_29.json"

STATUS = "THETA_RESIDUAL_CROSS_VALIDATION_STABILITY_RUN_EXECUTED"
THRESHOLD = 0.65

def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    if value == "":
        raise ValueError(f"missing numeric field {key}")
    return float(value)

def reduction_fraction(baseline_sse: float, theta_sse: float) -> float:
    if baseline_sse <= 0.0:
        return 0.0
    return (baseline_sse - theta_sse) / baseline_sse

def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"missing source CSV: {SOURCE.relative_to(ROOT)}")

    by_galaxy: dict[str, dict[str, float]] = defaultdict(lambda: {
        "row_count": 0.0,
        "baseline_sse": 0.0,
        "theta_sse": 0.0,
    })

    total_rows = 0
    total_baseline_sse = 0.0
    total_theta_sse = 0.0

    with SOURCE.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            galaxy_id = row["galaxy_id"]
            baseline_term = as_float(row, "baseline_squared_error_term")
            theta_term = as_float(row, "theta_squared_error_term")

            if baseline_term < 0.0:
                raise SystemExit(f"negative baseline term for {galaxy_id}")
            if theta_term < 0.0:
                raise SystemExit(f"negative theta term for {galaxy_id}")

            by_galaxy[galaxy_id]["row_count"] += 1.0
            by_galaxy[galaxy_id]["baseline_sse"] += baseline_term
            by_galaxy[galaxy_id]["theta_sse"] += theta_term

            total_rows += 1
            total_baseline_sse += baseline_term
            total_theta_sse += theta_term

    if total_rows == 0:
        raise SystemExit("no source rows found")
    if not by_galaxy:
        raise SystemExit("no galaxy folds found")
    if total_baseline_sse <= 0.0:
        raise SystemExit("nonpositive total baseline SSE")

    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

    fold_rows: list[dict[str, object]] = []
    fold_reductions: list[float] = []

    for galaxy_id in sorted(by_galaxy):
        fold = by_galaxy[galaxy_id]
        baseline_sse = float(fold["baseline_sse"])
        theta_sse = float(fold["theta_sse"])
        reduction = reduction_fraction(baseline_sse, theta_sse)
        fold_reductions.append(reduction)

        fold_rows.append({
            "heldout_galaxy_id": galaxy_id,
            "heldout_row_count": int(fold["row_count"]),
            "heldout_baseline_squared_error": baseline_sse,
            "heldout_theta_squared_error": theta_sse,
            "heldout_improvement": baseline_sse - theta_sse,
            "heldout_reduction_fraction": reduction,
            "heldout_passes_threshold": reduction >= THRESHOLD,
        })

    with CSV_OUT.open("w", newline="") as f:
        fieldnames = list(fold_rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(fold_rows)

    aggregate_reduction = reduction_fraction(total_baseline_sse, total_theta_sse)
    mean_fold_reduction = statistics.fmean(fold_reductions)
    median_fold_reduction = statistics.median(fold_reductions)
    min_fold_reduction = min(fold_reductions)
    threshold_passing_folds = sum(1 for x in fold_reductions if x >= THRESHOLD)

    artifact = {
        "status": STATUS,
        "source": str(SOURCE.relative_to(ROOT)),
        "output_csv": str(CSV_OUT.relative_to(ROOT)),
        "row_count": total_rows,
        "galaxy_count": len(by_galaxy),
        "fold_count": len(by_galaxy),
        "threshold_reduction_fraction": THRESHOLD,
        "total_baseline_squared_error": total_baseline_sse,
        "total_theta_squared_error": total_theta_sse,
        "total_improvement": total_baseline_sse - total_theta_sse,
        "aggregate_reduction_fraction": aggregate_reduction,
        "mean_fold_reduction_fraction": mean_fold_reduction,
        "median_fold_reduction_fraction": median_fold_reduction,
        "min_fold_reduction_fraction": min_fold_reduction,
        "threshold_passing_folds": threshold_passing_folds,
        "aggregate_passes_threshold": aggregate_reduction >= THRESHOLD,
        "mean_fold_passes_threshold": mean_fold_reduction >= THRESHOLD,
        "boundary": [
            "repository-archived theta residual cross-validation stability run only",
            "leave-one-galaxy-out accounting over archived theta output only",
            "no raw SPARC payload authenticity newly verified",
            "no authentic SPARC empirical validation",
            "no independent real-data holdout validation",
            "no predictive GDM law closure",
            "no low-parameter deficit-mass model closure",
            "no dark matter replacement claim",
            "no Lambda-CDM failure claim",
            "no physical validation claim",
            "no SPARC empirical victory claim",
            "no PhD-complete final result claim",
            "no unrestricted Chronos-RR",
            "no unrestricted H4.1/FGL",
            "no P vs NP",
            "no Clay problem",
        ],
    }

    ART.parent.mkdir(parents=True, exist_ok=True)
    with ART.open("w") as f:
        json.dump(artifact, f, indent=2, sort_keys=True)
        f.write("\n")

    print("THETA_RESIDUAL_CROSS_VALIDATION_STABILITY_RUN_EXECUTED")
    print(json.dumps({
        "row_count": artifact["row_count"],
        "galaxy_count": artifact["galaxy_count"],
        "fold_count": artifact["fold_count"],
        "aggregate_reduction_fraction": artifact["aggregate_reduction_fraction"],
        "mean_fold_reduction_fraction": artifact["mean_fold_reduction_fraction"],
        "median_fold_reduction_fraction": artifact["median_fold_reduction_fraction"],
        "min_fold_reduction_fraction": artifact["min_fold_reduction_fraction"],
        "threshold_passing_folds": artifact["threshold_passing_folds"],
        "aggregate_passes_threshold": artifact["aggregate_passes_threshold"],
        "mean_fold_passes_threshold": artifact["mean_fold_passes_threshold"],
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
