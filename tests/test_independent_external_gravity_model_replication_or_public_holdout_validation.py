import json
from pathlib import Path

PROV = Path("artifacts/gravity/goco06s_independent_external_gravity_vector_provenance_2026_05_30.json")
ART = Path("artifacts/gravity/independent_external_gravity_model_replication_or_public_holdout_validation_2026_05_30.json")

def test_goco06s_public_holdout_provenance():
    provenance = json.loads(PROV.read_text(encoding="utf-8"))
    assert provenance["source_name"] == "GOCO06s"
    assert provenance["source_doi"] == "10.5880/ICGEM.2019.002"
    assert len(provenance["source_gfc_sha256"]) == 64
    assert len(provenance["external_vector_sha256"]) == 64
    assert provenance["synthesis"]["numeric_rows_seen"] > 0
    assert provenance["synthesis"]["synthesis_terms_used"] > 0
    assert provenance["synthesis"]["raw_grid_std_before_normalization"] > 0
    assert provenance["shape"]["shape_compatible_with_baseline"] is True
    assert provenance["shape"]["shape_compatible_with_deficit"] is True

def test_independent_replication_or_public_holdout_artifact():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    assert artifact["status"] == "INDEPENDENT_PUBLIC_HOLDOUT_VALIDATION_EXECUTED_BOUNDARY_LOCKED"
    assert artifact["replication_or_public_holdout_validation_executed"] is True
    assert artifact["replication_source_name"] == "GOCO06s"
    assert artifact["replication_source_doi"] == "10.5880/ICGEM.2019.002"
    assert artifact["vector_length"] > 0
    assert artifact["lower_rmse_model"] in {"baseline", "deficit", "tie"}
    assert isinstance(artifact["replicates_prior_lower_rmse_model"], bool)

def test_independent_replication_or_public_holdout_boundaries():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    boundary = artifact["boundary"]
    assert boundary["replication_or_public_holdout_only"] is True
    assert boundary["comparison_only"] is True
    assert boundary["no_empirical_gravity_result_claim"] is True
    assert boundary["no_gr_failure_claim"] is True
    assert boundary["no_new_gravity_claim"] is True
    assert boundary["no_dark_matter_replacement_claim"] is True
    assert boundary["no_lambda_cdm_failure_claim"] is True
    assert boundary["no_quantum_gravity_claim"] is True
    assert boundary["no_clay_claim"] is True
    assert boundary["independent_validation_required_before_physical_claim"] is True
