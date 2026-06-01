import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/non_null_physical_model_vector_or_deficit_mass_derivation_target_2026_06_01.json")
DOC = Path("docs/status/NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_TARGET_2026_06_01.md")
VERIFY = Path("tools/verify_non_null_physical_model_vector_or_deficit_mass_derivation_target.py")

def test_artifact_records_target():
    data = json.loads(ART.read_text())
    assert data["object"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_TARGET"
    assert data["decision"] == "PASS"
    assert data["required_new_input"] == "NonNullPhysicalModelVectorOrDeficitMassDerivation"

def test_required_input_not_supplied():
    data = json.loads(ART.read_text())
    assert data["required_input_supplied"] is False
    assert data["current_model_kind"] == "aligned_zero_null_vector"
    assert data["current_model_is_physical"] is False

def test_acceptance_predicates_recorded():
    data = json.loads(ART.read_text())
    predicates = data["required_input_schema"]["acceptance_predicates"]
    assert "vector is not identically zero" in predicates
    assert "derivation or physical model definition is supplied" in predicates

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "target only" in doc
    assert "non-null physical model vector not supplied" in doc
    assert "current comparison remains null comparator only" in doc
    assert "no Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_TARGET_OK" in result.stdout
