from __future__ import annotations

"""Bounded isolated timings for exact polar angular normalization operations.

Rebuilds the raw density in memory, verifies its known srepr digest, then runs
together(reduced) and cancel(reduced) in separate forked processes. The large
preserved srepr is never parsed. Each operation has its own time limit and
resource receipt.
"""
import hashlib
import json
import multiprocessing
import resource
import signal
import time
from pathlib import Path

import sympy as sp
from gfe_polar_first_order_curvature_operator import build_first_order_operator
from gfe_polar_second_order_curvature_operator import build_second_order_operator
from gfe_polar_quadratic_density_coefficient import build_raw_quadratic_density

EXPECTED_RAW_SHA256 = "84a03f8caea6cce9f6730af986fcec49afca6b8288c88e9d22d72cd51639e005"
OUTPUT = Path("gfe_polar_normalization_benchmark.json")
OPERATION_LIMIT_SECONDS = 40 * 60
SERIALIZATION_LIMIT_SECONDS = 5 * 60


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


def alarm_timeout(_signum, _frame):
    raise TimeoutError("benchmark stage reached its configured wall-clock limit")


def isolated_worker(operation_name, expr, result_queue):
    operation = {"together": sp.together, "cancel": sp.cancel}[operation_name]
    baseline_rss = rss_kib()
    baseline_peak = peak_rss_kib()
    signal.signal(signal.SIGALRM, alarm_timeout)
    started = time.monotonic()
    signal.alarm(OPERATION_LIMIT_SECONDS)
    try:
        result = operation(expr)
    except TimeoutError as exc:
        signal.alarm(0)
        result_queue.put({
            "schema": "gfe-polar-normalization-benchmark-v1",
            "stage": operation_name,
            "status": "time_limit_reached",
            "passed": False,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "configured_limit_seconds": OPERATION_LIMIT_SECONDS,
            "rss_kib_before": baseline_rss,
            "rss_kib_at_limit": rss_kib(),
            "peak_rss_kib_before": baseline_peak,
            "peak_rss_kib_at_limit": peak_rss_kib(),
            "error": str(exc),
            "output_size_available": False,
        })
        return
    finally:
        signal.alarm(0)

    elapsed = time.monotonic() - started
    after_rss = rss_kib()
    after_peak = peak_rss_kib()
    serialization_started = time.monotonic()
    signal.alarm(SERIALIZATION_LIMIT_SECONDS)
    try:
        serialized = sp.srepr(result)
    except TimeoutError as exc:
        signal.alarm(0)
        result_queue.put({
            "schema": "gfe-polar-normalization-benchmark-v1",
            "stage": operation_name,
            "status": "serialization_time_limit_reached",
            "passed": False,
            "elapsed_seconds": round(elapsed, 3),
            "configured_serialization_limit_seconds": SERIALIZATION_LIMIT_SECONDS,
            "serialization_elapsed_seconds": round(time.monotonic() - serialization_started, 3),
            "rss_kib_before": baseline_rss,
            "rss_kib_after_operation": after_rss,
            "peak_rss_kib_before": baseline_peak,
            "peak_rss_kib_after_operation": after_peak,
            "peak_rss_growth_kib": max(0, after_peak - baseline_peak),
            "error": str(exc),
            "output_size_available": False,
        })
        return
    finally:
        signal.alarm(0)

    result_queue.put({
        "schema": "gfe-polar-normalization-benchmark-v1",
        "stage": operation_name,
        "status": "completed",
        "passed": True,
        "elapsed_seconds": round(elapsed, 3),
        "rss_kib_before": baseline_rss,
        "rss_kib_after_operation": after_rss,
        "peak_rss_kib_before": baseline_peak,
        "peak_rss_kib_after_operation": after_peak,
        "peak_rss_growth_kib": max(0, after_peak - baseline_peak),
        "serialization_elapsed_seconds": round(time.monotonic() - serialization_started, 3),
        "rss_kib_after_serialization": rss_kib(),
        "peak_rss_kib_after_serialization": peak_rss_kib(),
        "output_srepr_characters": len(serialized),
        "output_srepr_sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "output_size_available": True,
    })


def run_isolated(operation_name, expr):
    context = multiprocessing.get_context("fork")
    result_queue = context.Queue()
    process = context.Process(target=isolated_worker, args=(operation_name, expr, result_queue))
    process.start()
    process.join(OPERATION_LIMIT_SECONDS + SERIALIZATION_LIMIT_SECONDS + 60)
    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "schema": "gfe-polar-normalization-benchmark-v1",
            "stage": operation_name,
            "status": "process_time_limit_reached",
            "passed": False,
            "configured_limit_seconds": OPERATION_LIMIT_SECONDS + SERIALIZATION_LIMIT_SECONDS,
            "peak_rss_kib": None,
            "output_size_available": False,
            "error": "worker did not return before the parent safety limit",
        }
    if not result_queue.empty():
        return result_queue.get()
    return {
        "schema": "gfe-polar-normalization-benchmark-v1",
        "stage": operation_name,
        "status": "worker_exited_without_receipt",
        "passed": False,
        "exit_code": process.exitcode,
        "output_size_available": False,
    }


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
    reduced = raw / sp.sin(theta)
    receipt("normalization_benchmark_started", passed=True,
            input_sha256_srepr=digest,
            input_expression_srepr_characters=len(raw_srepr),
            operations=["together(reduced)", "cancel(reduced)"],
            per_operation_limit_seconds=OPERATION_LIMIT_SECONDS,
            per_serialization_limit_seconds=SERIALIZATION_LIMIT_SECONDS,
            total_wall_clock_limit_minutes=120)

    results = []
    for operation_name in ("together", "cancel"):
        receipt(operation_name + "_started", passed=True,
                input_sha256_srepr=digest,
                configured_limit_seconds=OPERATION_LIMIT_SECONDS,
                baseline_rss_kib=rss_kib(), baseline_peak_rss_kib=peak_rss_kib())
        result = run_isolated(operation_name, reduced)
        results.append(result)
        receipt(operation_name + "_result", **result)
    passed = all(item.get("passed") is True for item in results)
    receipt("normalization_benchmark_completed", passed=passed,
            input_sha256_srepr=digest,
            total_elapsed_seconds=round(time.monotonic() - started, 3),
            operation_results=[{k: v for k, v in item.items() if k != "schema"} for item in results],
            frontier="MEASURED_NORMALIZATION_COSTS" if passed else "MEASURED_LIMIT_OR_FAILURE",
            angular_integral_completed=False,
            polynomial_gate_completed=False,
            reference_81_slot_comparison_completed=False,
            quadratic_action_derived=False)
    if not passed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
