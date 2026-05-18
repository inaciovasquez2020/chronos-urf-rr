from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def test_naive_restricted_separator_lean_objects_present() -> None:
    text = read("lean/Chronos/Frontier/NaiveRestrictedPositiveEntropyDomainSeparator.lean")
    assert "def NaiveRestrictedPositiveEntropyDomainConstruction" in text
    assert "theorem naiveRestrictedPositiveEntropyDomainConstruction_refuted" in text
    assert "PositiveEntropyAdmissibleClassUniformWitness lam" in text
    assert "positiveEntropyAdmissibleClassUniformWitnessConstruction_refuted lam" in text


def test_naive_restricted_separator_imported() -> None:
    text = read("lean/Chronos.lean")
    assert "import Chronos.Frontier.NaiveRestrictedPositiveEntropyDomainSeparator" in text


def test_naive_restricted_separator_status_doc() -> None:
    text = read("docs/status/NAIVE_RESTRICTED_POSITIVE_ENTROPY_DOMAIN_SEPARATOR_2026_05_17.md")
    assert "Status: NEGATIVE_CLOSURE_ONLY" in text
    assert "naive restricted-domain route is refuted" in text
    assert "genuinely domain-indexed witness object" in text
    assert "Does not prove:" in text
    assert "genuine restricted positive-entropy domain construction" in text
    assert "P vs NP" in text
    assert "any Clay problem" in text


def test_naive_restricted_separator_artifact() -> None:
    data = json.loads(
        read("artifacts/chronos/naive_restricted_positive_entropy_domain_separator_2026_05_17.json")
    )
    assert data["status"] == "NEGATIVE_CLOSURE_ONLY"
    assert data["lean_definition"] == "NaiveRestrictedPositiveEntropyDomainConstruction"
    assert data["lean_theorem"] == "naiveRestrictedPositiveEntropyDomainConstruction_refuted"
    assert data["remaining_frontier"] == "genuine domain-indexed positive-entropy witness construction"


def test_naive_restricted_separator_no_overclaim() -> None:
    combined = "\n".join(
        read(path)
        for path in [
            "lean/Chronos/Frontier/NaiveRestrictedPositiveEntropyDomainSeparator.lean",
            "docs/status/NAIVE_RESTRICTED_POSITIVE_ENTROPY_DOMAIN_SEPARATOR_2026_05_17.md",
            "artifacts/chronos/naive_restricted_positive_entropy_domain_separator_2026_05_17.json",
        ]
    )
    forbidden = [
        "proves genuine restricted positive-entropy domain construction",
        "proves domain-indexed positive-entropy witness construction",
        "proves unrestricted RateThickFiberCoercivity",
        "proves unrestricted UniversalFiberEntropyGap",
        "proves unrestricted Chronos-RR",
        "proves H4.1/FGL",
        "proves P vs NP",
        "proves any Clay problem",
    ]
    for token in forbidden:
        assert token not in combined
