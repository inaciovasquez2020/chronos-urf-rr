from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_FILE = ROOT / "Chronos/Frontier/RepositoryNativeRankAmbientDatum.lean"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_rank_ambient_datum_2026_05_13.json"
VERIFIER = ROOT / "tools/verify_repository_native_rank_ambient_datum.py"


def test_lean_rank_ambient_surface_present() -> None:
    text = LEAN_FILE.read_text()
    assert "structure RepositoryNativeRankAmbientRecord" in text
    assert "structure VerifiedRepositoryNativeRankAmbientDatum" in text
    assert "def ChronosNativeRankAmbientDatumVerified : Prop :=" in text
    assert "theorem chronos_verified_rank_ambient_witness" in text
    assert "CONDITIONAL / EXTERNAL_DATA_ASSUMPTION_ONLY" in text


def test_artifact_boundary_and_record() -> None:
    data = json.loads(ARTIFACT.read_text())
    record = data["record"]

    assert data["status"] == "CONDITIONAL / EXTERNAL_DATA_ASSUMPTION_ONLY"
    assert data["theorem_level_closure"] is False
    assert data["terminal_missing_object"] == "ChronosNativeRankAmbientDatumVerified"

    assert record["carrierId"] == 0
    assert record["ambient"] > 0
    assert record["rank"] > 0
    assert record["rank"] <= record["ambient"]

    boundary = "\n".join(data["boundary"])
    assert "Metadata is not theorem-level source validity" in boundary
    assert "No unrestricted UniversalFiberEntropyGap theorem" in boundary
    assert "No P vs NP" in boundary
    assert "No Clay closure" in boundary


def test_verifier_passes() -> None:
    subprocess.run([sys.executable, str(VERIFIER)], cwd=ROOT, check=True)
