import json
from pathlib import Path

PROV = Path("artifacts/gravity/eigen6c4_external_gravity_vector_provenance_2026_05_30.json")
ART = Path("artifacts/gravity/authentic_external_gravity_model_comparison_result_2026_05_30.json")

def test_eigen6c4_external_vector_provenance():
    provenance = json.loads(PROV.read_text(encoding="utf-8"))
    assert provenance["source_name"] == "EIGEN-6C4"
    assert provenance["source_doi"] == "10.5880/icgem.2015.1"
    assert len(provenance["source_gfc_sha256"]) == 64
    assert len(provenance["external_vector_sha256"]) == 64
    assert provenance["shape"]["shape_compatible_with_baseline"] is True
    assert provenance["shape"]["shape_compatible_with_deficit"] is True

def test_external_gravity_model_comparison_result_artifact():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    assert artifact["status"] == "EXTERNAL_MODEL_COMPARISON_EXECUTED_BOUNDARY_LOCKED"
    assert artifact["comparison_executed"] is True
    assert artifact["external_source_name"] == "EIGEN-6C4"
    assert artifact["external_source_doi"] == "10.5880/icgem.2015.1"
    assert artifact["vector_length"] > 0
    assert artifact["lower_rmse_model"] in {"baseline", "deficit", "tie"}

def test_external_gravity_model_comparison_result_boundaries():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    boundary = artifact["boundary"]
    assert boundary["comparison_only"] is True
    assert boundary["no_external_gravity_model_fabrication"] is True
    assert boundary["no_empirical_gravity_result_claim"] is True
    assert boundary["no_gr_failure_claim"] is True
    assert boundary["no_new_gravity_claim"] is True
    assert boundary["no_dark_matter_replacement_claim"] is True
    assert boundary["no_lambda_cdm_failure_claim"] is True
    assert boundary["no_quantum_gravity_claim"] is True
    assert boundary["no_clay_claim"] is True
    assert boundary["independent_validation_required_before_physical_claim"] is True
