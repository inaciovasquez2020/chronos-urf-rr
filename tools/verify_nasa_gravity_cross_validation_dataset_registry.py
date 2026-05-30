#!/usr/bin/env python3
from pathlib import Path
import json
import re

ART = Path("artifacts/gravity/nasa_gravity_cross_validation_dataset_registry_2026_05_29.json")

REQUIRED = {
    "GRACEFO_L2_JPL_MONTHLY_0063",
    "TELLUS_GRAC-GRFO_MASCON_GRID_RL06.3_V4",
    "TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4",
    "GRC-GFO_GRIDDED_AOD1B_JPL_MASCON_RL06.3",
    "GLDAS_NOAH025_3H_2.1",
    "SPL4SMGP.008",
    "ATL06.007",
    "SWOT_L2_HR_RiverSP_2.0",
    "GPM_3IMERGDF.07",
    "MERRA2_SURFACE_ATMOSPHERE_PRODUCTS",
    "CDDIS_GNSS_SLR_PRODUCTS",
    "NASA_LAMBDA_CMB_PRODUCTS",
}

def fail(msg: str):
    raise SystemExit(msg)

if not ART.exists():
    fail(f"MISSING_REGISTRY_ARTIFACT: {ART}")

x = json.loads(ART.read_text())

if x.get("status") != "NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_CREATED":
    fail("BAD_STATUS")

datasets = x.get("datasets")
if not isinstance(datasets, list):
    fail("DATASETS_NOT_LIST")

if x.get("dataset_count") != 12 or len(datasets) != 12:
    fail("BAD_DATASET_COUNT")

names = {d.get("short_name") for d in datasets}
missing = REQUIRED - names
extra = names - REQUIRED

if missing:
    fail(f"MISSING_DATASETS: {sorted(missing)}")
if extra:
    fail(f"EXTRA_DATASETS: {sorted(extra)}")

for d in datasets:
    for field in [
        "short_name",
        "source_center",
        "source_url",
        "role",
        "registry_status",
        "downstream_gate",
    ]:
        if not isinstance(d.get(field), str) or not d[field]:
            fail(f"BAD_FIELD_{field}: {d}")

    if not re.match(r"^https://", d["source_url"]):
        fail(f"BAD_SOURCE_URL: {d['short_name']}")

    if d.get("registry_status") not in {
        "BOUND_AUTHENTICATED_PAYLOAD",
        "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND",
    }:
        fail(f"BAD_REGISTRY_STATUS: {d['short_name']}")

    if not isinstance(d.get("real_payload_required_before_use"), bool):
        fail(f"BAD_PAYLOAD_REQUIRED_FLAG: {d['short_name']}")

bound = [d for d in datasets if d["registry_status"] == "BOUND_AUTHENTICATED_PAYLOAD"]
unbound = [d for d in datasets if d["registry_status"] == "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"]

if len(bound) != 1:
    fail(f"EXPECTED_ONE_BOUND_DATASET_GOT_{len(bound)}")

if bound[0]["short_name"] != "GRACEFO_L2_JPL_MONTHLY_0063":
    fail("BOUND_DATASET_IS_NOT_GRACEFO_L2_JPL_MONTHLY_0063")

if len(unbound) != 11:
    fail(f"EXPECTED_ELEVEN_UNBOUND_DATASETS_GOT_{len(unbound)}")

required_next = x.get("required_next_payload_gates")
if not isinstance(required_next, list) or len(required_next) != 11:
    fail("BAD_REQUIRED_NEXT_PAYLOAD_GATES")

boundary = x.get("boundary")
if not isinstance(boundary, list):
    fail("BAD_BOUNDARY")

for forbidden_claim in [
    "no empirical falsification conclusion",
    "no GR failure claim",
    "no new gravity claim",
    "no dark matter replacement claim",
    "no Lambda-CDM failure claim",
    "no quantum gravity claim",
    "no Clay problem claim",
]:
    if forbidden_claim not in boundary:
        fail(f"MISSING_BOUNDARY_LOCK: {forbidden_claim}")

print("NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_OK")
print(json.dumps({
    "dataset_count": len(datasets),
    "bound_dataset_count": len(bound),
    "unbound_dataset_count": len(unbound),
    "artifact": ART.as_posix(),
}, indent=2))
