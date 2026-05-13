#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_FILE = ROOT / "Chronos/Frontier/RepositoryNativeRankAmbientDatum.lean"
SOURCE = ROOT / "artifacts/chronos/repository_native_rank_ambient_source_2026_05_13.json"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_rank_ambient_datum_2026_05_13.json"
THIS = Path(__file__).resolve()

REQUIRED_LEAN_TOKENS = [
    "structure RepositoryNativeRankAmbientRecord",
    "def RepositoryNativeRankAmbientRecordWellFormed",
    "def RepositoryNativeRankAmbientRecordMatches",
    "structure VerifiedRepositoryNativeRankAmbientDatum",
    "def ChronosNativeRankAmbientDatumVerified : Prop :=",
    "theorem chronos_verified_rank_ambient_witness",
    "CONDITIONAL / EXTERNAL_DATA_ASSUMPTION_ONLY",
    "No unrestricted UniversalFiberEntropyGap theorem",
    "No P vs NP",
    "No Clay closure",
]

FORBIDDEN_TOKENS = [
    "theorem ChronosNativeRankAmbientDatumVerified",
    "unconditional UniversalFiberEntropyGap",
    "unconditional P vs NP closure",
    "unconditional Clay closure",
    "unconditional Chronos-RR closure",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def load_source() -> dict:
    data = json.loads(SOURCE.read_text())
    required = {"carrierId", "index", "rank", "ambient", "boundary"}
    missing = required - set(data)
    assert not missing, f"source missing keys: {sorted(missing)}"
    assert data["carrierId"] == 0
    assert isinstance(data["index"], int)
    assert isinstance(data["rank"], int)
    assert isinstance(data["ambient"], int)
    assert data["ambient"] > 0
    assert data["rank"] > 0
    assert data["rank"] <= data["ambient"]
    return data


def expected_artifact() -> dict:
    src = load_source()
    record_core = {
        "carrierId": src["carrierId"],
        "index": src["index"],
        "rank": src["rank"],
        "ambient": src["ambient"],
        "sourcePath": str(SOURCE.relative_to(ROOT)),
        "sourceSha256": sha256_file(SOURCE),
        "extractorName": THIS.name,
        "extractorSha256": sha256_file(THIS),
    }
    record = dict(record_core)
    record["recordSha256"] = sha256_bytes(canonical_json(record_core))
    return {
        "status": "CONDITIONAL / EXTERNAL_DATA_ASSUMPTION_ONLY",
        "theorem_level_closure": False,
        "lean_module": "Chronos.Frontier.RepositoryNativeRankAmbientDatum",
        "terminal_missing_object": "ChronosNativeRankAmbientDatumVerified",
        "record": record,
        "verified_checks": [
            "source file hash recorded",
            "extractor file hash recorded",
            "record canonical hash recorded",
            "carrierId = 0",
            "0 < ambient",
            "0 < rank",
            "rank <= ambient",
        ],
        "boundary": [
            "Verified rank/ambient datum surface only",
            "Metadata is not theorem-level source validity",
            "Importer is not formalized in Lean",
            "No unconditional SemanticRankRateCertificate",
            "No unrestricted UniversalFiberEntropyGap theorem",
            "No Chronos-RR",
            "No H4.1/FGL",
            "No P vs NP",
            "No Clay closure",
        ],
    }


def verify_lean_surface() -> None:
    text = LEAN_FILE.read_text()
    for token in REQUIRED_LEAN_TOKENS:
        assert token in text, f"missing Lean token: {token}"
    for token in FORBIDDEN_TOKENS:
        assert token not in text, f"forbidden Lean token: {token}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    verify_lean_surface()
    expected = expected_artifact()

    if args.write:
        ARTIFACT.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")

    actual = json.loads(ARTIFACT.read_text())
    assert actual == expected, "artifact differs from verifier-derived expected artifact"

    print("RepositoryNativeRankAmbientDatum surface verified.")


if __name__ == "__main__":
    main()
