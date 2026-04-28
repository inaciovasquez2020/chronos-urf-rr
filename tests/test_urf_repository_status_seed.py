import json
from pathlib import Path

from tools.urf_status_classification import classify_repository


SEED = Path("docs/status/URF_REPOSITORY_STATUS_SEED_2026_04_28.json")


def _rows():
    return json.loads(SEED.read_text(encoding="utf-8"))["repositories"]


def test_seed_registry_exists_and_is_status_only():
    data = json.loads(SEED.read_text(encoding="utf-8"))

    assert data["status"] == "status-only seed registry"
    assert "does not imply theorem-level closure" in data["boundary"]


def test_seed_registry_has_required_repositories():
    names = {row["name"] for row in _rows()}

    assert "pachner-invariant" in names
    assert "cslib-fmt" in names
    assert "chronos-urf-rr" in names
    assert "urf-core" in names
    assert "urf-axioms" in names
    assert "poincare-new-derivation" in names
    assert "cyclone-terminal-obstruction" in names


def test_seed_registry_classification_outputs_are_bounded():
    classified = {row["name"]: classify_repository(row) for row in _rows()}

    assert classified["pachner-invariant"]["classification"] == "Solved theorem surface"
    assert (
        classified["cslib-fmt"]["classification"]
        == "Closed executable surface with placeholders"
    )
    assert (
        classified["chronos-urf-rr"]["classification"]
        == "Closed executable surface with placeholders"
    )
    assert classified["urf-core"]["classification"] == "Open formalization"
    assert classified["urf-axioms"]["classification"] == "Open formalization"
    assert classified["poincare-new-derivation"]["classification"] == "Open formalization"
    assert classified["cyclone-terminal-obstruction"]["classification"] == "Open formalization"


def test_no_seeded_boundary_repo_is_classified_as_solved():
    for row in _rows():
        classified = classify_repository(row)
        markers = (
            row.get("sorry_count", 0)
            + row.get("admit_count", 0)
            + row.get("axiom_count", 0)
            + row.get("true_placeholder_count", 0)
        )

        if markers > 0:
            assert classified["classification"] != "Solved theorem surface"
