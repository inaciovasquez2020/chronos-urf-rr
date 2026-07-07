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

REQUIRED_METADATA = {
    "live_days": 231,
    "exposure": "758 tonne day",
    "detector_medium": "liquid argon",
    "detector_mass_kg": 3279,
    "observed_candidate_signal_events": 0,
    "confidence_level": "90%",
    "reported_limit_100gev_cm2": "3.9e-45",
}

REQUIRED_FORBIDDEN_CLAIMS = [
    "dark matter solved",
    "gravity closure",
    "cosmology closure",
]

REQUIRED_NON_CLAIMS = [
    "Does not solve dark matter.",
    "Does not derive or close gravity.",
    "Does not prove cosmology closure.",
    "Does not transform a null result into a theory-complete result.",
    "Does not provide unrestricted physical closure.",
]

def fail(message: str) -> None:
    raise SystemExit(f"DEAP3600_EXTERNAL_NULL_RESULT_EVIDENCE_RECEIPT_FAIL: {message}")

def main() -> None:
    data = json.loads(RECEIPT.read_text())

    for key, expected in EXPECTED.items():
        if data.get(key) != expected:
            fail(f"{key} must equal {expected!r}")

    if data.get("dataset_checksum_status") != "NO_PUBLIC_MACHINE_READABLE_DATASET_CHECKSUM_PINNED":
        fail("dataset checksum boundary must remain explicit")

    metadata = data.get("source_metadata")
    if not isinstance(metadata, dict):
        fail("source_metadata must be an object")

    for key, expected in REQUIRED_METADATA.items():
        if metadata.get(key) != expected:
            fail(f"source_metadata.{key} must equal {expected!r}")

    if data.get("forbidden_claims") != REQUIRED_FORBIDDEN_CLAIMS:
        fail("forbidden_claims must exactly pin dark matter, gravity, and cosmology closure prohibitions")

    if data.get("non_claims") != REQUIRED_NON_CLAIMS:
        fail("non_claims must exactly preserve closure boundaries")

    allowed_use = data.get("allowed_use")
    if not isinstance(allowed_use, list) or "external validation evidence" not in allowed_use:
        fail("allowed_use must include external validation evidence")

    print("DEAP3600_EXTERNAL_NULL_RESULT_EVIDENCE_RECEIPT_OK")

if __name__ == "__main__":
    main()
