#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN_PATH = ROOT / "lean/Chronos/Frontier/LatentTraceEntropyRoute.lean"
DOC_PATH = ROOT / "docs/status/LATENT_TRACE_ENTROPY_ROUTE_2026_05_17.md"
ARTIFACT_PATH = ROOT / "artifacts/chronos/latent_trace_entropy_route_2026_05_17.json"

REQUIRED_LEAN = [
    "inductive LatentState",
    "inductive Trace",
    "def TraceProjection",
    "theorem traceProjection_noninjective",
    "def EmptyTraceFiberNonempty",
    "theorem trace_empty_not_absent",
    "def LatentTower",
    "def EntropyLoss",
    "structure DynamicalSystem",
    "def RateThickClass",
    "def RankRateBridgeLaw",
    "def RateThickFiberCoercivity",
    "theorem entropyFaithfulLowerEnvelope",
    "theorem universalFiberEntropyGap",
    "structure HyperbolicCoercivityCertificate",
    "theorem hyperbolicRoute",
 "theorem rateThickFiberCoercivity_refuted",
]

REQUIRED_DOC = [
    "CONDITIONAL_FRONTIER_ONLY",
    "Non-injectivity of a trace projection alone does not imply",
    "RankRateBridgeLaw λ",
    "RateThickFiberCoercivity λ",
 "rateThickFiberCoercivity_refuted",
    "Does not prove:",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

FORBIDDEN_LEAN = [
    "sorry",
    "admit",
    "axiom ",
]

FORBIDDEN_COMBINED = [
    "proves unrestricted universalfiberentropygap",
    "proves unrestricted chronos-rr",
    "proves h4.1/fgl",
    "proves p vs np",
    "solves p vs np",
    "solves a clay problem",
    "clay problem solved",
]

def main() -> None:
    lean = LEAN_PATH.read_text()
    doc = DOC_PATH.read_text()
    artifact = json.loads(ARTIFACT_PATH.read_text())

    for token in REQUIRED_LEAN:
        assert token in lean, token

    for token in FORBIDDEN_LEAN:
        assert token not in lean, token

    for token in REQUIRED_DOC:
        assert token in doc, token

    assert artifact["status"] == "CONDITIONAL_FRONTIER_ONLY"
    assert "RankRateBridgeLaw" in artifact["frontier_inputs"]
    assert "RateThickFiberCoercivity" in artifact["frontier_inputs"]
    assert "PositiveEntropyAdmissibleClass" in artifact["frontier_inputs"]
    assert "rateThickFiberCoercivity_refuted" in artifact["closed_surfaces"]

    chronos = (ROOT / "lean/Chronos.lean").read_text()
    assert "import Chronos.Frontier.LatentTraceEntropyRoute" in chronos

    combined = (lean + "\n" + doc + "\n" + json.dumps(artifact)).lower()
    for token in FORBIDDEN_COMBINED:
        assert token not in combined, token

    print("Latent trace entropy route verified.")

if __name__ == "__main__":
    main()
