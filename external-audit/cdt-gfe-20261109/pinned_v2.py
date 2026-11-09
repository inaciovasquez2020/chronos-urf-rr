"""CDT-SM-01 Stage 0 candidate classification, version 2.

The July 12, 2026 version 1 algorithm is immutable. Version 2 changes only
its null-control acceptance logic: C3 and C4 must EACH pass independently.
This is a synthetic-data classifier, not a physical detection.
"""
from statistics import fmean


def classify(rows, u_c, threshold):
    accepted = [row for row in rows if row["included"] is True]
    configurations = ("C1", "C2", "C3", "C4")
    grouped = {
        configuration: [
            row["eta"]
            for row in accepted
            if row["configuration"] == configuration
        ]
        for configuration in configurations
    }

    if any(not grouped[configuration] for configuration in configurations):
        return {"status": "PENDING"}

    means = {
        configuration: fmean(grouped[configuration])
        for configuration in configurations
    }

    swap_estimator = (means["C1"] - means["C2"]) / 2.0
    null_estimator = (means["C3"] + means["C4"]) / 2.0
    swap_reversal = means["C1"] * means["C2"] < 0.0
    null_control_pass = {
        configuration: abs(means[configuration]) < 2.0 * u_c
        for configuration in ("C3", "C4")
    }
    null_controls_pass = all(null_control_pass.values())

    candidate = (
        abs(swap_estimator) >= threshold
        and null_controls_pass
        and swap_reversal
    )

    return {
        "status": (
            "SINGLE_LAB_CANDIDATE_ONLY"
            if candidate
            else "NO_CANDIDATE"
        ),
        "means": means,
        "swap_estimator": swap_estimator,
        "null_estimator": null_estimator,
        "swap_reversal": swap_reversal,
        "null_control_pass": null_control_pass,
        "null_controls_pass": null_controls_pass,
    }
