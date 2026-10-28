from __future__ import annotations

"""Isolated timing and resource audit for exact polar angular normalization.

Rebuilds the raw density in memory and benchmarks the two operations in the
same order as the production path. The preserved srepr is never parsed.
"""
import hashlib
import json
import resource
import time
from pathlib import Path

import sympy as sp
from gfe_polar_first_order_curvature_operator import build_first_order_operator
from gfe_polar_second_order_curvature_operator import build_second_order_operator
from gfe_polar_quadratic_density_coefficient import build_raw_quadratic_density

EXPECTED_RAW_SHA256 = "84a03f8caea6cce9f6730af986fcec49afca6b8288c88e9d22d72cd51639e005"
OUTPUT = Path("gfe_polar_normalization_benchmark.json")


def rss_kib():
    try:
        for line in Path("/proc/self/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1])
    except OSError:
        pass
    return None


def peak_rss_kib():
    # Linux ru_maxrss is KiB; the GitHub Actions runner is Ubuntu.
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def receipt(stage, **fields):
    row = {"schema": "gfe-polar-normalization-benchmark-v1", "stage": stage, **fields}
    print(json.dumps(row, sort_keys=True, default=str), flush=True)
    with OUTPUT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, sort_keys=True, default=str) + "\n")


def measure_expression(stage, operation, expr):
    before_rss = rss_kib()
    before_peak = peak_rss_kib()
    started = time.monotonic()
    result = operation(expr)
    elapsed = time.monotonic() - started
    after_rss = rss_kib()
    after_peak = peak_rss_kib()
    receipt(
        stage + "_completed",
        passed=True,
        elapsed_seconds=round(elapsed, 3),
        rss_kib_before=before_rss,
        rss_kib_after=after_rss,
        peak_rss_kib_before=before_peak,
        peak_rss_kib_after_operation=after_peak,
        peak_rss_growth_kib=max(0, after_peak - before_peak),
        output_serialization_completed=False,
    )
    serialization_started = time.monotonic()
    serialized = sp.srepr(result)
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    output_chars = len(serialized)
    receipt(
        stage + "_output",
        passed=True,
        output_srepr_characters=output_chars,
        output_srepr_sha256=digest,
        serialization_elapsed_seconds=round(time.monotonic() - serialization_started, 3),
        rss_kib_after_serialization=rss_kib(),
        peak_rss_kib_after_serialization=peak_rss_kib(),
    )
    return result, output_chars


def main():
    OUTPUT.write_text("", encoding="utf-8")
    started = time.monotonic()
    receipt("raw_density_build_started", expected_sha256_srepr=EXPECTED_RAW_SHA256)
    first = build_first_order_operator()
    second = build_second_order_operator(first)
    data = build_raw_quadratic_density(first, second)
    raw = data["raw_epsilon_squared_density_coefficient"]
    raw_srepr = sp.srepr(raw)
    digest = hashlib.sha256(raw_srepr.encode("utf-8")).hexdigest()
    if digest != EXPECTED_RAW_SHA256:
        receipt("raw_density_integrity_gate", passed=False,
                expected_sha256_srepr=EXPECTED_RAW_SHA256, actual_sha256_srepr=digest)
        raise SystemExit("raw density digest mismatch; refusing to benchmark a different input")
    receipt("raw_density_integrity_gate", passed=True,
            sha256_srepr=digest, srepr_characters=len(raw_srepr),
            build_elapsed_seconds=round(time.monotonic() - started, 3),
            rss_kib=rss_kib(), peak_rss_kib=peak_rss_kib())

    theta = data["coordinates"][2]
    sine = sp.sin(theta)
    base = raw / sine
    receipt("normalization_benchmark_started", passed=True,
            input_sha256_srepr=digest,
            input_expression_srepr_characters=len(raw_srepr),
            order="together(raw/sin(theta)); cancel(together_result)",
            wall_clock_limit_minutes=120)

    together_result, together_chars = measure_expression("together", sp.together, base)
    cancel_result, cancel_chars = measure_expression(
        "cancel_after_together", sp.cancel, together_result
    )
    receipt("normalization_benchmark_completed", passed=True,
            input_sha256_srepr=digest,
            total_elapsed_seconds=round(time.monotonic() - started, 3),
            together_output_characters=together_chars,
            cancel_output_characters=cancel_chars,
            peak_rss_kib=peak_rss_kib(),
            frontier="MEASURED_NORMALIZATION_COSTS",
            angular_integral_completed=False,
            polynomial_gate_completed=False,
            reference_81_slot_comparison_completed=False,
            quadratic_action_derived=False)


if __name__ == "__main__":
    main()
