from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "tools/gfe/derive_gfe_corrected_pq_gqq.py"
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_pq_gqq.json"
SOURCE = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_laurent_generator.json"


def test_deterministic_corrected_pq_gqq_export() -> None:
    before = ARTIFACT.read_bytes()
    run = subprocess.run(
        ["python3", str(EXPORTER)], cwd=ROOT, check=True,
        capture_output=True, text=True, timeout=180,
    )
    assert "LEADING_COMMUTATOR := [G_-1,P0]=G_-1 != 0" in run.stdout
    assert "GQQ_EXACT := passed" in run.stdout
    assert "HISTORICAL_D_MATCH := corrected-different" in run.stdout
    assert ARTIFACT.read_bytes() == before


def test_exact_boundary_hash_and_classification() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert data["certificate"] == "GFE_CORRECTED_AEH_HALF_EXACT_PQ_GQQ"
    assert data["source_laurent_generator_sha256"] == hashlib.sha256(
        SOURCE.read_bytes()).hexdigest()
    assert data["projector_ranks"] == {"P0": 4, "Q0": 2}
    assert data["leading_commutator"] == "[G_-1,P0]=G_-1 != 0"
    assert data["ordinary_generator_guard"] == json.loads(
        SOURCE.read_text(encoding="utf-8"))["ordinary_generator_guard"]
    assert data["GQQ"]["rank_classification"] == (
        "rank 2 when Delta != 0; rank 1 when Delta = 0, throughout the ordinary-generator guard"
    )
    assert data["historical_D_check"]["status"] == "corrected-different"
    assert data["fredholm_obstruction_relation"]["status"] == "retained but not transferred"
    assert all(data["exact_checks"].values())
    payload_hash = data.pop("payload_sha256")
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(encoded).hexdigest() == payload_hash


def test_projectors_are_exact_coordinate_complements() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    p0 = [[int(value) for value in row] for row in data["P0"]]
    q0 = [[int(value) for value in row] for row in data["Q0"]]
    assert [p0[i][i] for i in range(6)] == [1, 1, 0, 1, 1, 0]
    assert [q0[i][i] for i in range(6)] == [0, 0, 1, 0, 0, 1]
    assert all(p0[i][j] + q0[i][j] == (1 if i == j else 0)
               for i in range(6) for j in range(6))
