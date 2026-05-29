#!/usr/bin/env python3
from pathlib import Path
import json
import re

DIGEST = Path("artifacts/gracefo/authenticated_gracefo_payload_digest_certificate_2026_05_29.json")
SCHEMA = Path("artifacts/gracefo/gracefo_schema_validation_execution_result_2026_05_29.json")

DATA_RE = re.compile(
    r"^(?P<product>GAA|GAB|GAC|GAD|GSM)-2_"
    r"(?P<start>\d{7})-(?P<end>\d{7})_"
    r"GRFO_JPLEM_"
    r"(?P<branch>BC01|BA01|BB01)_0603$"
)

REQUIRED_PER_PERIOD = {
    ("GAA", "BC01"),
    ("GAB", "BC01"),
    ("GAC", "BC01"),
    ("GAD", "BC01"),
    ("GSM", "BA01"),
    ("GSM", "BB01"),
}

def fail(message: str) -> None:
    raise SystemExit(message)

def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)

require(DIGEST.exists(), f"MISSING_DIGEST_ARTIFACT: {DIGEST}")
require(SCHEMA.exists(), f"MISSING_SCHEMA_ARTIFACT: {SCHEMA}")

digest = json.loads(DIGEST.read_text())
schema = json.loads(SCHEMA.read_text())

require(
    digest.get("status") == "AUTHENTICATED_GRACEFO_PAYLOAD_DIGEST_CERTIFICATE_CREATED",
    "DIGEST_CERTIFICATE_STATUS_NOT_CREATED",
)
require(
    schema.get("status") == "GRACEFO_SCHEMA_VALIDATION_EXECUTION_RESULT_CREATED",
    "SCHEMA_VALIDATION_STATUS_NOT_CREATED",
)
require(
    digest.get("dataset_short_name") == "GRACEFO_L2_JPL_MONTHLY_0063",
    "WRONG_DIGEST_DATASET",
)
require(
    schema.get("dataset_short_name") == "GRACEFO_L2_JPL_MONTHLY_0063",
    "WRONG_SCHEMA_DATASET",
)

collection_sha256 = digest.get("collection_sha256")
require(isinstance(collection_sha256, str), "MISSING_COLLECTION_SHA256")
require(re.fullmatch(r"[0-9a-f]{64}", collection_sha256) is not None, "INVALID_COLLECTION_SHA256")
require(schema.get("collection_sha256") == collection_sha256, "SCHEMA_DIGEST_SHA_MISMATCH")

entries = digest.get("files")
require(isinstance(entries, list), "DIGEST_FILES_NOT_LIST")
require(len(entries) == digest.get("file_count"), "DIGEST_FILE_COUNT_MISMATCH")
require(digest.get("total_bytes", 0) > 0, "DIGEST_TOTAL_BYTES_NOT_POSITIVE")

matched = []
for entry in entries:
    path = Path(entry.get("path", ""))
    name = path.name
    sha = entry.get("sha256")
    size = entry.get("bytes")

    require(isinstance(size, int) and size > 0, f"INVALID_FILE_SIZE: {name}")
    require(isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha), f"INVALID_FILE_SHA256: {name}")

    m = DATA_RE.match(name)
    if m:
        matched.append({
            "product": m.group("product"),
            "branch": m.group("branch"),
            "period": (m.group("start"), m.group("end")),
        })

periods = {}
for item in matched:
    periods.setdefault(item["period"], set()).add((item["product"], item["branch"]))

require(len(periods) == 2, f"UNEXPECTED_PERIOD_COUNT: {len(periods)}")
require(len(matched) == 12, f"UNEXPECTED_DATA_FILE_COUNT: {len(matched)}")

for period, keys in periods.items():
    missing = REQUIRED_PER_PERIOD - keys
    require(not missing, f"MISSING_REQUIRED_PRODUCTS_FOR_PERIOD_{period}: {sorted(missing)}")

checks = schema.get("schema_checks", {})
require(checks.get("period_count") == 2, "SCHEMA_PERIOD_COUNT_MISMATCH")
require(checks.get("data_file_count") == 12, "SCHEMA_DATA_FILE_COUNT_MISMATCH")
require(checks.get("required_monthly_products_present_per_period") is True, "SCHEMA_REQUIRED_PRODUCTS_FLAG_FALSE")
require(checks.get("payload_file_sha256_values_match_digest_artifact") is True, "SCHEMA_SHA_FLAG_FALSE")

print("GRACEFO_SCHEMA_VALIDATION_EXECUTION_RESULT_CI_PORTABLE_OK")
print(json.dumps({
    "period_count": len(periods),
    "data_file_count": len(matched),
    "digest_file_count": digest["file_count"],
    "total_bytes": digest["total_bytes"],
    "collection_sha256": collection_sha256,
}, indent=2))
