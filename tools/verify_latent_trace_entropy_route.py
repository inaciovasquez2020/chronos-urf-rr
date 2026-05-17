#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "lean/Chronos/Frontier/LatentTraceEntropyRoute.lean",
    ROOT / "docs/status/LATENT_TRACE_ENTROPY_ROUTE_2026_05_17.md",
    ROOT / "artifacts/chronos/latent_trace_entropy_route_2026_05_17.json",
]

REQUIRED = [
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
    "CONDITIONAL_FRONTIER_ONLY",
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

FORBIDDEN_CLAIMS = [
    "proves unrestricted UniversalFiberEntropyGap",
    "proves unrestricted Chronos-RR",
    "proves H4.1/FGL",
    "proves P vs NP",
    "solves P vs NP",
    "solves a Clay problem",
    "Clay problem solved",
]

missing = [str(p.relative_to(ROOT)) for p in FILES if not p.exists()]
assert not missing, f"Missing files: {missing}"

lean = FILES[0].read_text()
combined = "\n".join(p.read_text() for p in FILES)
lowered = combined.lower()

for token in REQUIRED:
    assert token.lower() in lowered, token

for token in FORBIDDEN_LEAN:
    assert token not in lean, token

for token in FORBIDDEN_CLAIMS:
    assert token.lower() not in lowered, token

artifact = json.loads(FILES[2].read_text())
assert artifact["status"] == "CONDITIONAL_FRONTIER_ONLY"
assert "RankRateBridgeLaw" in artifact["frontier_inputs"]
assert "RateThickFiberCoercivity" in artifact["frontier_inputs"]

chronos = (ROOT / "lean/Chronos.lean").read_text()
assert (
    "import Chronos.Frontier.LatentTraceEntropyRoute" in chronos
), "missing Chronos.lean import"

print("Latent trace entropy route verified.")
