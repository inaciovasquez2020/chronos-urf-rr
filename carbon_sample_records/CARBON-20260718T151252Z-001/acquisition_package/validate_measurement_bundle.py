#!/usr/bin/env python3

import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path

PLACEHOLDERS = {
    "",
    "PENDING",
    "PLACEHOLDER",
    "PROPOSED",
    "TBD",
    "UNKNOWN",
    "NULL",
    "NONE",
    "N/A",
    "NA",
}

METADATA_REQUIRED = (
    "sample_id",
    "material",
    "measurement_status",
    "shape",
    "mass_kg",
    "mass_uncertainty_kg",
    "radius_m",
    "radius_uncertainty_m",
    "temperature_k",
    "temperature_uncertainty_k",
    "observer_radius_m",
    "observer_radius_uncertainty_m",
    "ct_instrument",
    "ct_calibration_id",
    "ct_calibration_date",
    "density_calibration_method",
    "stress_instrument",
    "stress_calibration_id",
    "stress_calibration_date",
    "acquisition_timestamp",
    "provenance",
)

CT_COLUMNS = (
    "r_m",
    "rho_kg_m3",
    "rho_uncertainty_kg_m3",
)

STRESS_COLUMNS = (
    "r_m",
    "sigma_rr_pa",
    "sigma_tt_pa",
    "sigma_rr_uncertainty_pa",
    "sigma_tt_uncertainty_pa",
)


def missing(value):
    if value is None:
        return True

    if isinstance(value, str):
        return value.strip().upper() in PLACEHOLDERS

    if isinstance(value, float):
        return not math.isfinite(value)

    return False


def finite_number(value, field):
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc

    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")

    return result


def validate_metadata(path, expected_sample_id):
    data = json.loads(path.read_text())

    if not isinstance(data, dict):
        raise ValueError("metadata root must be a JSON object")

    for field in METADATA_REQUIRED:
        if field not in data or missing(data[field]):
            raise ValueError(f"missing calibrated metadata field: {field}")

    if data["sample_id"] != expected_sample_id:
        raise ValueError(
            f"sample_id must equal {expected_sample_id}"
        )

    if data["measurement_status"] != "MEASURED":
        raise ValueError("measurement_status must equal MEASURED")

    if data["shape"] != "sphere":
        raise ValueError("shape must equal sphere")

    positive_fields = (
        "mass_kg",
        "radius_m",
        "temperature_k",
        "observer_radius_m",
    )

    nonnegative_fields = (
        "mass_uncertainty_kg",
        "radius_uncertainty_m",
        "temperature_uncertainty_k",
        "observer_radius_uncertainty_m",
    )

    for field in positive_fields:
        if finite_number(data[field], field) <= 0.0:
            raise ValueError(f"{field} must be positive")

    for field in nonnegative_fields:
        if finite_number(data[field], field) < 0.0:
            raise ValueError(f"{field} must be nonnegative")

    if float(data["observer_radius_m"]) <= float(data["radius_m"]):
        raise ValueError(
            "observer_radius_m must exceed specimen radius_m"
        )

    timestamp = str(data["acquisition_timestamp"]).replace(
        "Z",
        "+00:00",
    )

    parsed = datetime.fromisoformat(timestamp)

    if parsed.tzinfo is None:
        raise ValueError(
            "acquisition_timestamp must include a timezone"
        )

    return data


def validate_csv(path, expected_columns):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)

        if reader.fieldnames != list(expected_columns):
            raise ValueError(
                f"{path.name} header must be: "
                + ",".join(expected_columns)
            )

        rows = list(reader)

    if len(rows) < 4:
        raise ValueError(
            f"{path.name} requires at least four measured rows"
        )

    previous_radius = None

    for row_number, row in enumerate(rows, start=2):
        for column in expected_columns:
            raw = str(row.get(column, "")).strip()

            if raw.upper() in PLACEHOLDERS:
                raise ValueError(
                    f"{path.name}:{row_number}:{column} is missing"
                )

            value = finite_number(
                raw,
                f"{path.name}:{row_number}:{column}",
            )

            if (
                "uncertainty" in column
                and value < 0.0
            ):
                raise ValueError(
                    f"{path.name}:{row_number}:{column} "
                    "must be nonnegative"
                )

        radius = float(row["r_m"])

        if radius < 0.0:
            raise ValueError(
                f"{path.name}:{row_number}:r_m must be nonnegative"
            )

        if (
            previous_radius is not None
            and radius <= previous_radius
        ):
            raise ValueError(
                f"{path.name} radii must be strictly increasing"
            )

        previous_radius = radius

    return rows


def main():
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: validate_measurement_bundle.py "
            "SAMPLE_DIRECTORY SAMPLE_ID"
        )

    directory = Path(sys.argv[1])
    sample_id = sys.argv[2]

    metadata = validate_metadata(
        directory / "sample_metadata.json",
        sample_id,
    )

    ct_rows = validate_csv(
        directory / "ct_density.csv",
        CT_COLUMNS,
    )

    stress_rows = validate_csv(
        directory / "residual_stress.csv",
        STRESS_COLUMNS,
    )

    metadata_radius = float(metadata["radius_m"])
    ct_radius = float(ct_rows[-1]["r_m"])
    stress_radius = float(stress_rows[-1]["r_m"])
    radius_uncertainty = float(
        metadata["radius_uncertainty_m"]
    )

    tolerance = max(5.0 * radius_uncertainty, 1.0e-12)

    if abs(ct_radius - metadata_radius) > tolerance:
        raise ValueError(
            "terminal CT radius does not agree with metadata radius"
        )

    if abs(stress_radius - metadata_radius) > tolerance:
        raise ValueError(
            "terminal stress radius does not agree with metadata radius"
        )

    print("RESULT := calibrated measurement bundle validated")
    print(f"SAMPLE_ID := {sample_id}")
    print(f"CT_ROWS := {len(ct_rows)}")
    print(f"STRESS_ROWS := {len(stress_rows)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"MISSING_OBJECT := {exc}") from exc
