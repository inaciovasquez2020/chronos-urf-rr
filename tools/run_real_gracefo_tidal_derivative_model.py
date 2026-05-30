#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import re

SCHEMA = Path("artifacts/gracefo/gracefo_schema_validation_execution_result_2026_05_29.json")
OUT = Path("artifacts/gracefo/real_gracefo_tidal_derivative_model_run_2026_05_29.json")

DATA_RE = re.compile(
    r"^(?P<product>GAA|GAB|GAC|GAD|GSM)-2_"
    r"(?P<start>\d{7})-(?P<end>\d{7})_"
    r"GRFO_JPLEM_"
    r"(?P<branch>BC01|BA01|BB01)_0603$"
)

def yday_to_date(s: str) -> datetime:
    year = int(s[:4])
    doy = int(s[4:])
    return datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=doy - 1)

def parse_float(x: str):
    try:
        return float(x.replace("D", "E").replace("d", "E"))
    except ValueError:
        return None

def parse_coefficients(path: Path):
    coeffs = {}
    for raw in path.read_text(errors="ignore").splitlines():
        parts = raw.split()
        if len(parts) < 5:
            continue

        tag = parts[0].upper()
        if tag not in {"GRCOF2", "GRCOF3", "GFC", "GFCT"}:
            continue

        try:
            degree = int(parts[1])
            order = int(parts[2])
        except ValueError:
            continue

        c = parse_float(parts[3])
        s = parse_float(parts[4])
        if c is None or s is None:
            continue

        coeffs[(degree, order, "C")] = c
        coeffs[(degree, order, "S")] = s

    return coeffs

def fail(msg: str):
    raise SystemExit(msg)

if not SCHEMA.exists():
    fail(f"MISSING_SCHEMA_ARTIFACT: {SCHEMA}")

schema = json.loads(SCHEMA.read_text())
if schema.get("status") != "GRACEFO_SCHEMA_VALIDATION_EXECUTION_RESULT_CREATED":
    fail("SCHEMA_VALIDATION_RESULT_NOT_CREATED")

matched = schema.get("matched_payload_files", [])
if not matched:
    fail("SCHEMA_ARTIFACT_HAS_NO_MATCHED_PAYLOAD_FILES")

records = []
for item in matched:
    path = Path(item["path"])
    if not path.exists():
        fail(f"MISSING_REAL_PAYLOAD_FILE: {path}")

    name = path.name
    m = DATA_RE.match(name)
    if not m:
        continue

    coeffs = parse_coefficients(path)
    degree2 = {
        f"{degree}:{order}:{kind}": value
        for (degree, order, kind), value in coeffs.items()
        if degree == 2
    }

    b = path.read_bytes()
    records.append({
        "path": path.as_posix(),
        "product": m.group("product"),
        "branch": m.group("branch"),
        "start_day": m.group("start"),
        "end_day": m.group("end"),
        "period_midpoint_utc": (
            yday_to_date(m.group("start"))
            + (yday_to_date(m.group("end")) - yday_to_date(m.group("start"))) / 2
        ).isoformat(),
        "sha256": hashlib.sha256(b).hexdigest(),
        "bytes": len(b),
        "coefficient_count": len(coeffs),
        "degree2_coefficient_count": len(degree2),
        "degree2": degree2,
    })

if len(records) != 12:
    fail(f"UNEXPECTED_REAL_PAYLOAD_RECORD_COUNT: {len(records)}")

by_key = {}
for rec in records:
    key = (rec["product"], rec["branch"])
    by_key.setdefault(key, []).append(rec)

product_runs = []
for key, rs in sorted(by_key.items()):
    rs = sorted(rs, key=lambda x: x["start_day"])
    if len(rs) != 2:
        fail(f"EXPECTED_TWO_PERIODS_FOR_PRODUCT_BRANCH_{key}_GOT_{len(rs)}")

    a, b = rs
    keys = sorted(set(a["degree2"]) & set(b["degree2"]))
    if not keys:
        fail(f"NO_SHARED_DEGREE2_COEFFICIENTS_FOR_{key}")

    deltas = [b["degree2"][k] - a["degree2"][k] for k in keys]
    delta_norm = math.sqrt(sum(x * x for x in deltas))
    max_abs_delta = max(abs(x) for x in deltas)

    ta = datetime.fromisoformat(a["period_midpoint_utc"])
    tb = datetime.fromisoformat(b["period_midpoint_utc"])
    dt_days = abs((tb - ta).total_seconds()) / 86400.0
    if dt_days <= 0:
        fail(f"NONPOSITIVE_PERIOD_SEPARATION_FOR_{key}")

    product_runs.append({
        "product": key[0],
        "branch": key[1],
        "period_a": [a["start_day"], a["end_day"]],
        "period_b": [b["start_day"], b["end_day"]],
        "midpoint_separation_days": dt_days,
        "shared_degree2_keys": keys,
        "shared_degree2_count": len(keys),
        "degree2_delta_norm": delta_norm,
        "degree2_max_abs_delta": max_abs_delta,
        "tidal_derivative_coefficient": delta_norm / dt_days,
        "units": "normalized_spherical_harmonic_degree2_delta_per_day",
    })

aggregate = {
    "product_branch_count": len(product_runs),
    "mean_tidal_derivative_coefficient": sum(x["tidal_derivative_coefficient"] for x in product_runs) / len(product_runs),
    "max_tidal_derivative_coefficient": max(x["tidal_derivative_coefficient"] for x in product_runs),
    "min_tidal_derivative_coefficient": min(x["tidal_derivative_coefficient"] for x in product_runs),
    "mean_degree2_delta_norm": sum(x["degree2_delta_norm"] for x in product_runs) / len(product_runs),
}

result = {
    "status": "REAL_GRACEFO_TIDAL_DERIVATIVE_MODEL_RUN_CREATED",
    "dataset_short_name": "GRACEFO_L2_JPL_MONTHLY_0063",
    "input_schema_artifact": SCHEMA.as_posix(),
    "collection_sha256": schema["collection_sha256"],
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "model": {
        "name": "finite_degree2_month_to_month_tidal_derivative_proxy",
        "definition": "For each GRACEFO product branch with two monthly periods, parse degree-2 normalized spherical harmonic coefficients and compute the Euclidean month-to-month coefficient-change norm divided by midpoint separation in days.",
        "scope": "real-data finite execution proxy only",
    },
    "period_count": 2,
    "payload_record_count": len(records),
    "product_branch_count": len(product_runs),
    "product_runs": product_runs,
    "aggregate": aggregate,
    "boundary": [
        "real GRACEFO payload model execution only",
        "finite degree-2 month-to-month tidal-derivative proxy only",
        "no empirical falsification conclusion",
        "no GR failure claim",
        "no new gravity claim",
        "no dark matter replacement claim",
        "no Lambda-CDM failure claim",
        "no unrestricted Chronos-RR claim",
        "no H4.1/FGL claim",
        "no P vs NP claim",
        "no Clay problem claim"
    ],
}

OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

print("REAL_GRACEFO_TIDAL_DERIVATIVE_MODEL_RUN_CREATED")
print(json.dumps({
    "payload_record_count": result["payload_record_count"],
    "product_branch_count": result["product_branch_count"],
    "mean_tidal_derivative_coefficient": result["aggregate"]["mean_tidal_derivative_coefficient"],
    "max_tidal_derivative_coefficient": result["aggregate"]["max_tidal_derivative_coefficient"],
    "artifact": OUT.as_posix(),
}, indent=2))
