from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def test_positive_entropy_uniform_witness_refutation_in_lean() -> None:
    text = read("lean/Chronos/Frontier/LatentTraceEntropyRoute.lean")
    assert "def PositiveEntropyAdmissibleClassUniformWitnessConstruction" in text
    assert "Nonempty (PositiveEntropyAdmissibleClassUniformWitness lam)" in text
    assert "theorem positiveEntropyAdmissibleClassUniformWitnessConstruction_refuted" in text
    assert "rateThickFiberCoercivity_refuted lam" in text
    assert "rateThickFiberCoercivity_from_positiveEntropyAdmissibleClassUniformWitness lam w" in text


def test_positive_entropy_uniform_witness_refutation_documented() -> None:
    text = read("docs/status/LATENT_TRACE_ENTROPY_ROUTE_2026_05_17.md")
    assert "Positive-entropy uniform witness construction refutation" in text
    assert "Negative closure only" in text
    assert "RestrictedPositiveEntropyDomainConstruction" in text
    assert "restricted positive-entropy domain construction" in text
    assert "unrestricted UniversalFiberEntropyGap" in text
    assert "P vs NP" in text
    assert "any Clay problem" in text


def test_positive_entropy_uniform_witness_refutation_artifact() -> None:
    data = json.loads(read("artifacts/chronos/latent_trace_entropy_route_2026_05_17.json"))
    block = data["positive_entropy_uniform_witness_construction_refutation"]
    assert block["status"] == "NEGATIVE_CLOSURE_ONLY"
    assert block["lean_def"] == "PositiveEntropyAdmissibleClassUniformWitnessConstruction"
    assert block["lean_theorem"] == "positiveEntropyAdmissibleClassUniformWitnessConstruction_refuted"
    assert block["remaining_frontier_input"] == "RestrictedPositiveEntropyDomainConstruction"


def test_no_forbidden_positive_entropy_overclaim() -> None:
    combined = "\n".join(
        read(path)
        for path in [
            "lean/Chronos/Frontier/LatentTraceEntropyRoute.lean",
            "docs/status/LATENT_TRACE_ENTROPY_ROUTE_2026_05_17.md",
            "artifacts/chronos/latent_trace_entropy_route_2026_05_17.json",
        ]
    )
    forbidden = [
        "proves restricted positive-entropy domain construction",
        "proves unrestricted RateThickFiberCoercivity",
        "proves unrestricted UniversalFiberEntropyGap",
        "proves unrestricted Chronos-RR",
        "proves H4.1/FGL",
        "proves P vs NP",
        "proves any Clay problem",
    ]
    for token in forbidden:
        assert token not in combined
