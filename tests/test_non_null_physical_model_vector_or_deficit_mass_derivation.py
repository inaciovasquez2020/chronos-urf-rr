import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/non_null_physical_model_vector_or_deficit_mass_derivation_2026_06_01.json")
DOC = Path("docs/status/NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_2026_06_01.md")
VERIFY = Path("tools/verify_non_null_physical_model_vector_or_deficit_mass_derivation.py")

def test_artifact_records_non_null_derivation():
    data = json.loads(ART.read_text())
    assert data["object"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION"
    assert data["decision"] == "PASS"
    assert data["target_required_input_supplied"] is True

def test_vector_is_non_null():
    data = json.loads(ART.read_text())
    vec = data["non_null_physical_model_vector_or_deficit_mass_derivation"]
    assert vec["vector_kind"] == "surface_mass_density_kg_m2"
    assert vec["vector_length"] == len(vec["values"])
    assert vec["nonzero_entry_count"] > 0

def test_acceptance_predicates_all_true():
    data = json.loads(ART.read_text())
    assert all(data["acceptance_predicates"].values())

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "not an independent predictive DFM-MKC model" in doc
    assert "not an empirical validation result" in doc
    assert "requires a fresh comparison run" in doc
    assert "no Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_OK" in result.stdout
