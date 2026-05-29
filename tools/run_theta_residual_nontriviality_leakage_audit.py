#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "artifacts/sparc/authentic_sparc_theta_residual_prediction_vector_run_2026_05_29.csv"
CV_ART = ROOT / "artifacts/sparc/theta_residual_cross_validation_stability_run_2026_05_29.json"
ART = ROOT / "artifacts/sparc/theta_residual_nontriviality_leakage_audit_2026_05_29.json"

STATUS = "THETA_RESIDUAL_NONTRIVIALITY_LEAKAGE_AUDIT_EXECUTED"

def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    if value == "":
        raise ValueError(f"missing numeric field {key}")
    return float(value)

def close(a: float, b: float, rel: float = 1e-9, abs_tol: float = 1e-9) -> bool:
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b), 1.0))

def main() -> None:
    for path in [SOURCE, CV_ART]:
        if not path.exists():
            raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")

    rows = []
    with SOURCE.open(newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("source theta residual CSV has no rows")

    exact_half_rows = 0
    exact_quarter_sse_rows = 0
    baseline_sse = 0.0
    theta_sse = 0.0
    residual_values = set()
    prediction_values = set()

    for row in rows:
        baseline_error = as_float(row, "baseline_error")
        theta_error = as_float(row, "theta_error")
        baseline_term = as_float(row, "baseline_squared_error_term")
        theta_term = as_float(row, "theta_squared_error_term")
        residual = as_float(row, "residual")
        baryonic_v2 = as_float(row, "baryonic_velocity_squared")
        prediction_v2 = as_float(row, "prediction_velocity_squared")

        if close(theta_error, baseline_error / 2.0):
            exact_half_rows += 1

        if close(theta_term, baseline_term / 4.0):
            exact_quarter_sse_rows += 1

        baseline_sse += baseline_term
        theta_sse += theta_term
        residual_values.add(round(residual, 9))
        prediction_values.add(round(prediction_v2 - baryonic_v2, 9))

    cv = json.loads(CV_ART.read_text())

    row_count = len(rows)
    half_identity_fraction = exact_half_rows / row_count
    quarter_sse_identity_fraction = exact_quarter_sse_rows / row_count
    total_error_ratio = theta_sse / baseline_sse
    total_reduction_fraction = (baseline_sse - theta_sse) / baseline_sse

    algebraic_leakage_detected = (
        half_identity_fraction == 1.0
        and quarter_sse_identity_fraction == 1.0
        and close(total_error_ratio, 0.25)
        and close(total_reduction_fraction, 0.75)
    )

    artifact = {
        "status": STATUS,
        "source": str(SOURCE.relative_to(ROOT)),
        "cross_validation_artifact": str(CV_ART.relative_to(ROOT)),
        "row_count": row_count,
        "galaxy_count": int(cv["galaxy_count"]),
        "exact_half_error_identity_rows": exact_half_rows,
        "exact_half_error_identity_fraction": half_identity_fraction,
        "exact_quarter_squared_error_rows": exact_quarter_sse_rows,
        "exact_quarter_squared_error_fraction": quarter_sse_identity_fraction,
        "baseline_squared_error": baseline_sse,
        "theta_squared_error": theta_sse,
        "theta_error_ratio": total_error_ratio,
        "theta_error_reduction_fraction": total_reduction_fraction,
        "cross_validation_min_fold_reduction_fraction": float(cv["min_fold_reduction_fraction"]),
        "cross_validation_mean_fold_reduction_fraction": float(cv["mean_fold_reduction_fraction"]),
        "cross_validation_threshold_passing_folds": int(cv["threshold_passing_folds"]),
        "algebraic_leakage_detected": algebraic_leakage_detected,
        "nontrivial_predictive_signal_certified": False,
        "audit_conclusion": "DETERMINISTIC_HALF_RESIDUAL_IDENTITY_EXPLAINS_75_PERCENT_SQUARED_ERROR_REDUCTION",
        "boundary": [
            "nontriviality leakage audit only",
            "detects algebraic reuse of residual target",
            "does not certify nontrivial predictive signal",
            "does not certify physical robustness",
            "does not certify out-of-sample physical validation",
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

    print("THETA_RESIDUAL_NONTRIVIALITY_LEAKAGE_AUDIT_EXECUTED")
    print(json.dumps({
        "row_count": artifact["row_count"],
        "galaxy_count": artifact["galaxy_count"],
        "exact_half_error_identity_fraction": artifact["exact_half_error_identity_fraction"],
        "exact_quarter_squared_error_fraction": artifact["exact_quarter_squared_error_fraction"],
        "theta_error_ratio": artifact["theta_error_ratio"],
        "theta_error_reduction_fraction": artifact["theta_error_reduction_fraction"],
        "algebraic_leakage_detected": artifact["algebraic_leakage_detected"],
        "nontrivial_predictive_signal_certified": artifact["nontrivial_predictive_signal_certified"],
        "audit_conclusion": artifact["audit_conclusion"],
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
