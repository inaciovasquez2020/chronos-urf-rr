from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/FiniteWitnessTheoremCluster.lean"
DOC = ROOT / "docs/status/FINITE_WITNESS_THEOREM_CLUSTER_2026_05_17.md"
ARTIFACT = ROOT / "artifacts/chronos/finite_witness_theorem_cluster_2026_05_17.json"


def test_verifier_passes() -> None:
    subprocess.run(
        ["python3", "tools/verify_finite_witness_theorem_cluster.py"],
        cwd=ROOT,
        check=True,
    )


def test_lean_file_has_no_unproved_tokens() -> None:
    text = LEAN.read_text()
    for token in ["sorry", "admit", "axiom", "unsafe"]:
        assert token not in text


def test_status_boundary_is_narrow() -> None:
    text = DOC.read_text()
    assert "PROVED_FINITE_THEOREM_CLUSTER_ONLY" in text
    assert "Finite witness certification only." in text
    assert "unrestricted UniversalFiberEntropyGap" in text
    assert "unrestricted Chronos-RR" in text
    assert "P vs NP" in text
    assert "any Clay problem" in text


def test_artifact_lists_all_theorems_and_defs() -> None:
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "PROVED_FINITE_THEOREM_CLUSTER_ONLY"
    assert data["lean_module"] == "Chronos.Frontier.FiniteWitnessTheoremCluster"
    for theorem in [
        "finite_carrier_nonempty_of_positive",
        "certificate_to_exists",
        "exists_to_certificate_nonempty",
        "certificate_nonempty_iff_exists",
        "certificate_map_nonempty",
        "exists_map",
        "true_certificate_nonempty_of_positive",
        "true_exists_of_positive",
    ]:
        assert theorem in data["proved_theorems"]
    for definition in [
        "certificate_map",
        "true_certificate_of_positive",
    ]:
        assert definition in data["data_definitions"]
