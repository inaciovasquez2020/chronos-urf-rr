#!/usr/bin/env python3
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/chronos/all_registered_carrier_subdominance.json"

LAMBDA_MIN = 1
LAMBDA_MAX = 250

def obs_dim(lam: int) -> int:
    return lam * lam + lam + 1

REGISTERED_ADMISSIBLE_CARRIERS = {
    "constant_capacity": lambda lam: 12,
    "log_capacity": lambda lam: math.ceil(8 * math.log2(lam + 1)),
    "linear_capacity": lambda lam: 3 * lam + 5,
    "affine_high_capacity": lambda lam: 11 * lam + 17,
    "n_log_n_capacity": lambda lam: math.ceil(lam * math.log2(lam + 1)),
    "quadratic_deficient_capacity": lambda lam: lam * lam,
}

REGISTERED_FORBIDDEN_CARRIERS = {
    "obstruction_oracle_capacity": lambda lam: obs_dim(lam),
    "obstruction_plus_one_capacity": lambda lam: obs_dim(lam) + 1,
}

def eventual_threshold(rows):
    for row in rows:
        start = row["lambda"]
        if all(r["subdominant"] for r in rows if r["lambda"] >= start):
            return start
    return None

carrier_results = []

for name, fn in REGISTERED_ADMISSIBLE_CARRIERS.items():
    rows = []
    for lam in range(LAMBDA_MIN, LAMBDA_MAX + 1):
        o = obs_dim(lam)
        t = fn(lam)
        rows.append({
            "lambda": lam,
            "obs_dim": o,
            "transcript_capacity": t,
            "subdominant": t < o,
        })

    threshold = eventual_threshold(rows)
    carrier_results.append({
        "name": name,
        "admissible": True,
        "eventual_subdominance_verified_on_range": threshold is not None,
        "holds_from_lambda": threshold,
        "rows": rows,
    })

for name, fn in REGISTERED_FORBIDDEN_CARRIERS.items():
    rows = []
    for lam in range(LAMBDA_MIN, LAMBDA_MAX + 1):
        o = obs_dim(lam)
        t = fn(lam)
        rows.append({
            "lambda": lam,
            "obs_dim": o,
            "transcript_capacity": t,
            "subdominant": t < o,
        })

    carrier_results.append({
        "name": name,
        "admissible": False,
        "reason_for_exclusion": "obstruction-oracle carrier can encode obstruction at full rank or higher",
        "eventual_subdominance_verified_on_range": False,
        "holds_from_lambda": None,
        "rows": rows,
    })

payload = {
    "status": "ALL_REGISTERED_CARRIERS_SIMULATED_ONLY",
    "theorem_closure": False,
    "uniform_carrier_subdominance_proved": False,
    "registered_admissible_carriers_all_pass": all(
        r["eventual_subdominance_verified_on_range"]
        for r in carrier_results
        if r["admissible"]
    ),
    "forbidden_oracle_carriers_present_as_boundary_tests": True,
    "missing_theorem": "Simulator-to-Universal-Carrier Lemma",
    "boundary": "This verifies all registered simulator carriers only; it does not quantify over all admissible mathematical carriers.",
    "lambda_range": [LAMBDA_MIN, LAMBDA_MAX],
    "obs_dim_model": "lambda^2 + lambda + 1",
    "carrier_results": carrier_results,
}

OUT.write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps(payload, indent=2))
