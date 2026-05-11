#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

LEAN_FILE = ROOT / "Chronos/Frontier/ZeroArityCarrierExhaustivenessConditional.lean"
ARTIFACT = ROOT / "artifacts/chronos/zero_arity_carrier_exhaustiveness_conditional.json"
DOC = ROOT / "docs/status/CHRONOS_ZERO_ARITY_CARRIER_EXHAUSTIVENESS_CONDITIONAL_2026_05_11.md"
NUMERICAL = ROOT / "tools/numerical_zero_arity_carrier_exhaustiveness.py"

REQUIRED_LEAN_TOKENS = [
    "structure CarrierData",
    "inductive Registry",
    "def RegistryGenerates",
    "def FiniteRegistry",
    "def RepresentedZeroArityRegistryPair",
    "def IsFiniteRepresentedAtom",
    "theorem represented_zero_arity_registry_pair_of_arity_zero",
    "theorem finite_registry_carrier",
    "theorem finite_represented_atom_of_finite_registry",
    "theorem CarrierRegistryGeneration",
    "theorem ZeroArityRegistryRepresentation",
    "theorem RegistryGeneratedAtomsFinite",
    "theorem ZeroArityCarrierExhaustiveness",
    "CONDITIONAL_SURFACE_ONLY",
]

REQUIRED_DOC_TOKENS = [
    "Status: CONDITIONAL_SURFACE_ONLY.",
    "This is a local `CarrierData` model.",
    "This is not unrestricted Chronos-RR closure.",
    "This is not H4.1/FGL closure.",
    "This is not UniversalFiberEntropyGap closure.",
    "This is not P vs NP closure.",
    "This is not Clay-problem closure.",
]

FORBIDDEN_TOKENS = [
    "unrestricted Chronos-RR is closed",
    "H4.1/FGL is closed",
    "UniversalFiberEntropyGap is closed",
    "P vs NP is solved",
    "Clay problem is solved",
    "theorem-level closure achieved",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"verification failed: {message}", file=sys.stderr)
        raise SystemExit(1)


def main() -> int:
    for path in [LEAN_FILE, ARTIFACT, DOC, NUMERICAL]:
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    lean_text = LEAN_FILE.read_text()
    doc_text = DOC.read_text()
    numerical_text = NUMERICAL.read_text()
    artifact = json.loads(ARTIFACT.read_text())

    for token in REQUIRED_LEAN_TOKENS:
        require(token in lean_text, f"Lean token missing: {token}")

    for token in REQUIRED_DOC_TOKENS:
        require(token in doc_text, f"doc token missing: {token}")

    combined = "\n".join([lean_text, doc_text, numerical_text, ARTIFACT.read_text()])
    for token in FORBIDDEN_TOKENS:
        require(token not in combined, f"forbidden overclaim token present: {token}")

    require(artifact["status"] == "CONDITIONAL_SURFACE_ONLY", "artifact status mismatch")
    require(artifact["theorem_level_closure"] is False, "artifact theorem closure must be false")
    require(artifact["unrestricted_chronos_rr_closure"] is False, "Chronos-RR closure must be false")
    require(artifact["h4_1_fgl_closure"] is False, "H4.1/FGL closure must be false")
    require(artifact["p_vs_np_closure"] is False, "P vs NP closure must be false")
    require(artifact["clay_problem_closure"] is False, "Clay closure must be false")

    print("Zero-arity carrier exhaustiveness conditional surface verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
