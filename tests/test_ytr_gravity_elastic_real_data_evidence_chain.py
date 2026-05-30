import subprocess
import sys


def run(path: str) -> None:
    subprocess.run([sys.executable, path], check=True)


def test_authentic_dataset_payload_binding() -> None:
    run("tools/verify_authentic_ytr_gravity_elastic_dataset_payload_binding.py")


def test_schema_validation_run() -> None:
    run("tools/verify_ytr_gravity_elastic_schema_validation_run.py")


def test_prediction_vector_real_data_run() -> None:
    run("tools/verify_ytr_gravity_elastic_prediction_vector_real_data_run.py")


def test_baseline_comparison_run() -> None:
    run("tools/verify_ytr_gravity_elastic_baseline_comparison_run.py")


def test_heldout_evidence_certificate() -> None:
    run("tools/verify_ytr_gravity_elastic_heldout_evidence_certificate.py")
