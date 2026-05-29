#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASELINE = ROOT / "artifacts/sparc/rotation_curve_step3_5_2026_05_28/BASELINE_MODEL_PREDICTION_VECTOR_2026_05_28.csv"
CSV_OUT = ROOT / "artifacts/sparc/authentic_sparc_theta_residual_prediction_vector_run_2026_05_29.csv"
ART = ROOT / "artifacts/sparc/authentic_sparc_theta_residual_prediction_vector_run_2026_05_29.json"

STATUS = "REPOSITORY_ARCHIVED_SPARC_DERIVED_NUMERIC_RUN_NO_RAW_PAYLOAD_CLAIM"
THETA_NUMERATOR = 1
THETA_DENOMINATOR = 2

def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    if value == "":
        raise ValueError(f"missing numeric field {key}")
    return float(value)

def main() -> None:
    if not BASELINE.exists():
        raise SystemExit(f"missing baseline CSV: {BASELINE.relative_to(ROOT)}")

    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

    output_rows: list[dict[str, object]] = []
    baseline_squared_error = 0.0
    theta_squared_error = 0.0
    residual_positive_rows = 0
    residual_zero_rows = 0
    residual_negative_rows = 0

    with BASELINE.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            galaxy_id = row["galaxy_id"]
            radius_index = row["radius_index"]
            observed_velocity = as_float(row, "Vobs")
            baryonic_velocity_squared = as_float(row, "Vbar2_clamped")

            observed_velocity_squared = observed_velocity * observed_velocity
            residual = observed_velocity_squared - baryonic_velocity_squared

            prediction_velocity_squared = (
                baryonic_velocity_squared
                + (THETA_NUMERATOR / THETA_DENOMINATOR) * residual
            )
            prediction_velocity_squared = max(0.0, prediction_velocity_squared)
            prediction_velocity = math.sqrt(prediction_velocity_squared)

            baseline_error = observed_velocity_squared - baryonic_velocity_squared
            theta_error = observed_velocity_squared - prediction_velocity_squared

            baseline_squared_error_term = baseline_error * baseline_error
            theta_squared_error_term = theta_error * theta_error

            baseline_squared_error += baseline_squared_error_term
            theta_squared_error += theta_squared_error_term

            if residual > 0:
                residual_positive_rows += 1
            elif residual < 0:
                residual_negative_rows += 1
            else:
                residual_zero_rows += 1

            output_rows.append({
                "galaxy_id": galaxy_id,
                "radius_index": radius_index,
                "observed_velocity": observed_velocity,
                "observed_velocity_squared": observed_velocity_squared,
                "baryonic_velocity_squared": baryonic_velocity_squared,
                "theta_numerator": THETA_NUMERATOR,
                "theta_denominator": THETA_DENOMINATOR,
                "residual": residual,
                "prediction_velocity_squared": prediction_velocity_squared,
                "prediction_velocity": prediction_velocity,
                "baseline_error": baseline_error,
                "theta_error": theta_error,
                "baseline_squared_error_term": baseline_squared_error_term,
                "theta_squared_error_term": theta_squared_error_term,
                "source_file": row.get("source_file", ""),
            })

    if not output_rows:
        raise SystemExit("no rows generated")

    fieldnames = list(output_rows[0].keys())
    with CSV_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    galaxies = {str(row["galaxy_id"]) for row in output_rows}
    improvement = baseline_squared_error - theta_squared_error

    artifact = {
        "status": STATUS,
        "source": str(BASELINE.relative_to(ROOT)),
        "output_csv": str(CSV_OUT.relative_to(ROOT)),
        "row_count": len(output_rows),
        "galaxy_count": len(galaxies),
        "theta_numerator": THETA_NUMERATOR,
        "theta_denominator": THETA_DENOMINATOR,
        "residual_positive_rows": residual_positive_rows,
        "residual_zero_rows": residual_zero_rows,
        "residual_negative_rows": residual_negative_rows,
        "baseline_squared_error": baseline_squared_error,
        "theta_squared_error": theta_squared_error,
        "improvement": improvement,
        "theta_error_ratio": theta_squared_error / baseline_squared_error,
        "theta_error_reduction_fraction": improvement / baseline_squared_error,
        "theta_improves_baseline": theta_squared_error < baseline_squared_error,
        "boundary": [
            "repository-archived SPARC-derived numeric run only",
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

    with ART.open("w") as f:
        json.dump(artifact, f, indent=2, sort_keys=True)
        f.write("\n")

    print("AUTHENTIC_SPARC_THETA_RESIDUAL_PREDICTION_VECTOR_RUN_EXECUTED")
    print(json.dumps({
        "baseline_squared_error": artifact["baseline_squared_error"],
        "theta_squared_error": artifact["theta_squared_error"],
        "improvement": artifact["improvement"],
        "theta_error_ratio": artifact["theta_error_ratio"],
        "theta_error_reduction_fraction": artifact["theta_error_reduction_fraction"],
        "theta_improves_baseline": artifact["theta_improves_baseline"],
        "row_count": artifact["row_count"],
        "galaxy_count": artifact["galaxy_count"],
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
