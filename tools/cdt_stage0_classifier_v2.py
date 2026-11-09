"""CDT-SM-01 Stage 0 candidate classification, version 2.

The frozen July 12, 2026 v1 algorithm is immutable. Version 2 retains
independent C3/C4 null-control checks and adds fail-closed row validation.
Synthetic-only software: four rows per configuration never certify the
16 authenticated blocks, accepted hours, blind key, or run authorization.
"""
import math
from statistics import fmean

CONFIGURATIONS = ("C1", "C2", "C3", "C4")
MIN_ACCEPTED_ROWS_PER_CONFIGURATION = 4


def _finite_number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except (ValueError, TypeError, OverflowError):
        return False


def _invalid(reason):
    return {"status": "INVALID_INPUT", "reason": reason,
            "execution_scope": "SYNTHETIC_ONLY"}


def classify(rows, u_c, threshold):
    if not _finite_number(u_c) or not _finite_number(threshold):
        return _invalid("nonfinite_or_nonnumeric_budget")
    if u_c <= 0 or threshold <= 0:
        return _invalid("nonpositive_budget")
    if not isinstance(rows, (list, tuple)):
        return _invalid("rows_not_sequence")

    grouped = {configuration: [] for configuration in CONFIGURATIONS}
    for row in rows:
        if not isinstance(row, dict):
            return _invalid("row_not_mapping")
        if not all(key in row for key in ("configuration", "eta", "included")):
            return _invalid("missing_row_field")
        if type(row["configuration"]) is not str or row["configuration"] not in CONFIGURATIONS:
            return _invalid("unknown_configuration")
        if type(row["included"]) is not bool:
            return _invalid("invalid_inclusion_flag")
        if not _finite_number(row["eta"]):
            return _invalid("nonfinite_or_nonnumeric_eta")
        if row["included"]:
            grouped[row["configuration"]].append(row["eta"])

    if any(len(grouped[c]) < MIN_ACCEPTED_ROWS_PER_CONFIGURATION
           for c in CONFIGURATIONS):
        return {"status": "PENDING", "execution_scope": "SYNTHETIC_ONLY"}

    try:
        means = {c: fmean(grouped[c]) for c in CONFIGURATIONS}
        signal_product = means["C1"] * means["C2"]
        swap_estimator = (means["C1"] - means["C2"]) / 2.0
        null_estimator = (means["C3"] + means["C4"]) / 2.0
        null_limit = 2.0 * u_c
    except (ArithmeticError, ValueError, TypeError):
        return _invalid("arithmetic_failure")

    if not all(_finite_number(x) for x in
               (*means.values(), signal_product, swap_estimator,
                null_estimator, null_limit)):
        return _invalid("nonfinite_derived_statistic")

    # The product is retained for an overflow guard, but must not determine
    # reversal: opposite finite signs can multiply to negative zero.
    swap_reversal = (
        (means["C1"] > 0.0 > means["C2"]) or
        (means["C2"] > 0.0 > means["C1"])
    )
    null_control_pass = {
        c: abs(means[c]) < null_limit for c in ("C3", "C4")
    }
    null_controls_pass = all(null_control_pass.values())
    candidate = (
        abs(swap_estimator) >= threshold and
        null_controls_pass and swap_reversal
    )
    return {
        "status": "SINGLE_LAB_CANDIDATE_ONLY" if candidate else "NO_CANDIDATE",
        "execution_scope": "SYNTHETIC_ONLY",
        "means": means,
        "swap_estimator": swap_estimator,
        "null_estimator": null_estimator,
        "swap_reversal": swap_reversal,
        "null_control_pass": null_control_pass,
        "null_controls_pass": null_controls_pass,
    }
