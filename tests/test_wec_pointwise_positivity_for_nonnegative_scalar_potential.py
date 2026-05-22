import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/WECPointwisePositivityForNonnegativeScalarPotential.lean"
ARTIFACT = ROOT / "artifacts/chronos/wec_pointwise_positivity_for_nonnegative_scalar_potential_2026_05_22.json"
DOC = ROOT / "docs/status/WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL_2026_05_22.md"

def test_wec_pointwise_positivity_artifact_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["id"] == "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL"
    assert data["status"] == "ADMISSIBLE_LEMMA_PROVED_ALGEBRAIC_ONLY"

def test_corrected_name_rejects_preservation_language():
    data = json.loads(ARTIFACT.read_text())
    assert data["corrected_naming"]["rejected_name"] == "WEC_POINTWISE_PRESERVATION_FOR_NONNEGATIVE_SCALAR_POTENTIAL"
    assert data["corrected_naming"]["accepted_name"] == "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL"
    assert "not dynamical preservation" in data["corrected_naming"]["reason"]

def test_lean_theorems_are_present_and_no_sorry():
    text = LEAN.read_text()
    assert "theorem wec_pointwise_positivity_for_nonnegative_scalar_potential" in text
    assert "theorem scalarFieldEnergyDensity_nonneg" in text
    assert "sorry" not in text.lower()
    assert "admit" not in text.lower()

def test_open_blockers_are_preserved():
    data = json.loads(ARTIFACT.read_text())
    assert "NON_SYMMETRIC_EINSTEIN_SCALAR_CONTINUATION_CRITERION_OPEN" in data["open_blockers"]
    assert "RAYCHAUDHURI_FOCUSING_WITH_SHEAR_CONTROL_OPEN" in data["open_blockers"]
    assert "NON_SYMMETRIC_TRAPPED_SURFACE_TRIGGER_FROM_CONCENTRATION_OPEN" in data["open_blockers"]

def test_no_overclaim_boundaries_are_preserved():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    assert "no PDE evolution theorem" in boundary
    assert "no finite-time collapse theorem" in boundary
    assert "no trapped-surface existence theorem" in boundary
    assert "no unrestricted gravity closure" in boundary
    assert "no cosmic censorship proof" in boundary
    assert "no hoop conjecture proof" in boundary
    assert "no Clay problem closure" in boundary

def test_status_doc_records_limits():
    text = DOC.read_text()
    assert "does not prove PDE evolution" in text
    assert "does not prove WEC preservation under time evolution" in text
    assert "does not prove finite-time collapse" in text
    assert "does not prove trapped-surface existence" in text
