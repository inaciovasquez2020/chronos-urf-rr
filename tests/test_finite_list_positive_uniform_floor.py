from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_verifier_passes():
    subprocess.run(["python3", "tools/verify_finite_list_positive_uniform_floor.py"], cwd=ROOT, check=True)

def test_files_present():
    assert (ROOT / "lean/Chronos/Frontier/FiniteListPositiveUniformFloor.lean").exists()
    assert (ROOT / "docs/status/FINITE_LIST_POSITIVE_UNIFORM_FLOOR_2026_05_18.md").exists()
    assert (ROOT / "artifacts/chronos/finite_list_positive_uniform_floor_2026_05_18.json").exists()

def test_lean_surface_contains_real_theorem():
    text = (ROOT / "lean/Chronos/Frontier/FiniteListPositiveUniformFloor.lean").read_text()
    assert "theorem finite_list_positive_uniform_floor" in text
    assert "masses ≠ []" in text
    assert "∀ x, x ∈ masses → 0 < x" in text
    assert "∃ ε : ℝ, 0 < ε ∧ ∀ x, x ∈ masses → ε ≤ x" in text
    assert "theorem FiniteSupportPositiveMassUniformFloor_list" in text
    assert "lt_min" in text
    assert "min_le_left" in text
    assert "min_le_right" in text
    assert "sorry" not in text
    assert "admit" not in text
    assert "axiom" not in text

def test_boundary_doc():
    text = (ROOT / "docs/status/FINITE_LIST_POSITIVE_UNIFORM_FLOOR_2026_05_18.md").read_text()
    assert "Status: `FINITE_LIST_POSITIVE_UNIFORM_FLOOR_PROVED`" in text
    assert "list-coded finite support only" in text
    assert "no unrestricted UniversalFiberEntropyGap" in text
    assert "no unrestricted Chronos-RR" in text
    assert "no unrestricted H4.1/FGL" in text
    assert "no P vs NP" in text
    assert "no Clay closure" in text

def test_artifact_status_and_boundary():
    data = json.loads((ROOT / "artifacts/chronos/finite_list_positive_uniform_floor_2026_05_18.json").read_text())
    assert data["status"] == "FINITE_LIST_POSITIVE_UNIFORM_FLOOR_PROVED"
    assert data["lean_theorem"] == "FiniteSupportPositiveMassUniformFloor_list"
    assert "nonempty finite list of positive real masses -> positive uniform lower floor" in data["closed"]
    assert "list-coded finite support only" in data["boundary"]
    assert "no unrestricted UniversalFiberEntropyGap" in data["boundary"]
    assert "no unrestricted Chronos-RR" in data["boundary"]
    assert "no unrestricted H4.1/FGL" in data["boundary"]
    assert "no P vs NP" in data["boundary"]
    assert "no Clay closure" in data["boundary"]
