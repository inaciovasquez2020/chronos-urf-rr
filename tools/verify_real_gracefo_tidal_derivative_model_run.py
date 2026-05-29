#!/usr/bin/env python3
from pathlib import Path
import json
import math

ART = Path("artifacts/gracefo/real_gracefo_tidal_derivative_model_run_2026_05_29.json")

def fail(msg: str):
    raise SystemExit(msg)

if not ART.exists():
    fail(f"MISSING_MODEL_RUN_ARTIFACT: {ART}")

x = json.loads(ART.read_text())

if x.get("status") != "REAL_GRACEFO_TIDAL_DERIVATIVE_MODEL_RUN_CREATED":
    fail("BAD_STATUS")

if x.get("dataset_short_name") != "GRACEFO_L2_JPL_MONTHLY_0063":
    fail("BAD_DATASET")

if x.get("period_count") != 2:
    fail("BAD_PERIOD_COUNT")

if x.get("payload_record_count") != 12:
    fail("BAD_PAYLOAD_RECORD_COUNT")

if x.get("product_branch_count") != 6:
    fail("BAD_PRODUCT_BRANCH_COUNT")

runs = x.get("product_runs")
if not isinstance(runs, list) or len(runs) != 6:
    fail("BAD_PRODUCT_RUNS")

for run in runs:
    if run.get("shared_degree2_count", 0) <= 0:
        fail("NO_SHARED_DEGREE2_KEYS")
    for k in [
        "degree2_delta_norm",
        "degree2_max_abs_delta",
        "tidal_derivative_coefficient",
        "midpoint_separation_days",
    ]:
        v = run.get(k)
        if not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0:
            fail(f"BAD_NUMERIC_FIELD: {k}")

agg = x.get("aggregate", {})
for k in [
    "mean_tidal_derivative_coefficient",
    "max_tidal_derivative_coefficient",
    "min_tidal_derivative_coefficient",
    "mean_degree2_delta_norm",
]:
    v = agg.get(k)
    if not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0:
        fail(f"BAD_AGGREGATE_FIELD: {k}")

print("REAL_GRACEFO_TIDAL_DERIVATIVE_MODEL_RUN_OK")
print(json.dumps({
    "period_count": x["period_count"],
    "payload_record_count": x["payload_record_count"],
    "product_branch_count": x["product_branch_count"],
    "mean_tidal_derivative_coefficient": agg["mean_tidal_derivative_coefficient"],
}, indent=2))
