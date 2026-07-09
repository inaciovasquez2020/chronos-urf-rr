#!/usr/bin/env python3
import json
from pathlib import Path

RECEIPT = Path(
    "artifacts/status/kepler_all_window_segment_family_post_merge_validation_receipt_2026_07_07.json"
)

def main():
    if not RECEIPT.exists():
        raise SystemExit("KEPLER_ALL_WINDOW_POST_MERGE_RECEIPT_FAIL: missing receipt")

    data = json.loads(RECEIPT.read_text())

    if data.get("receipt_name") != "KeplerAllWindowSegmentFamilyPostMergeValidationReceipt":
        raise SystemExit(
            "KEPLER_ALL_WINDOW_POST_MERGE_RECEIPT_FAIL: receipt_name mismatch"
        )

    print("KEPLER_ALL_WINDOW_POST_MERGE_RECEIPT_OK")

if __name__ == "__main__":
    main()
