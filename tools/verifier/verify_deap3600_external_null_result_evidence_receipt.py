#!/usr/bin/env python3
import json
from pathlib import Path

RECEIPT = Path("artifacts/status/deap3600_external_null_result_evidence_receipt_2026_07_07.json")

EXPECTED = {
    "claim_classification": "EXTERNAL_NULL_RESULT_OR_BACKGROUND_EVIDENCE_ONLY",
    "experiment": "DEAP-3600",
    "facility": "SNOLAB",
    "arxiv_id": "1902.04048",
    "arxiv_doi": "10.48550/arXiv.1902.04048",
    "related_publication_doi": "10.1103/PhysRevD.100.022004",
    "journal_reference": "Phys. Rev. D 100, 022004 (2019)",
    "source_url": "https://arxiv.org/abs/1902.04048",
}

FORBIDDEN_ASSERTIVE_PHRASES = [
    "dark matter solved",
    "solves dark matter",
    "gravity closure",
    "closes gravity",
    "cosmology closure",
    "closes cosmology",
    "unrestricted physical closure",
]

REQUIRED_NON_CLAIMS = [
    "Does not solve dark matter.",
    "Does not derive or close gravity.",
    "Does not prove cosmology closure.",
    "Does not transform a null result into a theory-complete result.",
    "Does not provide unrestricted physical closure.",
]

def fail(msg: str) -> None:
    raise SystemExit(f"DEAP3600_EXTERNAL_NULL_RESULT_EVIDENCE_RECEIPT_FAIL: {msg}")

def walk_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_strings(item)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            yield str(key)
            yield from walk_strings(value)

def main() -> None:
    if not RECEIPT.exists():
        fail(f"missing {RECEIPT}")

    data = json.loads(RECEIPT.read_text())

    for key, value in EXPECTED.items():
        if data.get(key) != value:
            fail(f"{key} must equal {value!r}")

    source_metadata = data.get("source_metadata")
    if not isinstance(source_metadata, dict):
        fail("source_metadata must be an object")

    required_metadata = {
        "live_days": 231,
        "exposure": "758 tonne day",
        "detector_medium": "liquid argon",
        "detector_mass_kg": 3279,
        "observed_candidate_signal_events": 0,
        "confidence_level": "90%",
        "reported_limit_100gev_cm2": "3.9e-45",
    }

    for key, value in required_metadata.items():
        if source_metadata.get(key) != value:
            fail(f"source_metadata.{key} must equal {value!r}")

    if data.get("dataset_checksum_status") != "NO_PUBLIC_MACHINE_READABLE_DATASET_CHECKSUM_PINNED":
        fail("dataset_checksum_status must preserve missing machine-readable dataset checksum boundary")

    forbidden_claims = data.get("forbidden_claims")
    if forbidden_claims != ["dark matter solved", "gravity closure", "cosmology closure"]:
        fail("forbidden_claims must pin the three prohibited closure phrases exactly")

    non_claims = data.get("non_claims")
    if non_claims != REQUIRED_NON_CLAIMS:
        fail("non_claims must preserve all closure boundaries exactly")

    allowed_use = data.get("allowed_use")
    if not isinstance(allowed_use, list) or "external validation evidence" not in allowed_use:
        fail("allowed_use must include external validation evidence")

    all_text = "\n".join(walk_strings(data)).lower()
    for phrase in FORBIDDEN_ASSERTIVE_PHRASES:
        if phrase in all_text and phrase not in [x.lower() for x in forbidden_claims]:
            if phrase not in "\n".join(x.lower() for x in REQUIRED_NON_CLAIMS):
                fail(f"forbidden assertive phrase escaped guard: {phrase}")

    print("DEAP3600_EXTERNAL_NULL_RESULT_EVIDENCE_RECEIPT_OK")

if __name__ == "__main__":
    main()
