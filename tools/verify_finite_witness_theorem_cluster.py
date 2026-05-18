#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/FiniteWitnessTheoremCluster.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/FINITE_WITNESS_THEOREM_CLUSTER_2026_05_17.md"
ARTIFACT = ROOT / "artifacts/chronos/finite_witness_theorem_cluster_2026_05_17.json"

REQUIRED_THEOREMS = [
    "finite_carrier_nonempty_of_positive",
    "certificate_to_exists",
    "exists_to_certificate_nonempty",
    "certificate_nonempty_iff_exists",
    "certificate_map_nonempty",
    "exists_map",
    "true_certificate_nonempty_of_positive",
    "true_exists_of_positive",
]

REQUIRED_DEFS = [
    "certificate_map",
    "true_certificate_of_positive",
]

FORBIDDEN_LEAN_TOKENS = [
    "sorry",
    "admit",
    "axiom",
    "unsafe",
]

REQUIRED_BOUNDARY_PHRASES = [
    "PROVED_FINITE_THEOREM_CLUSTER_ONLY",
    "Finite witness certification only.",
    "Does not prove:",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
    "any physics or cosmology closure",
]


def main() -> None:
    for path in [LEAN, CHRONOS, DOC, ARTIFACT]:
        if not path.exists():
            raise SystemExit(f"missing required file: {path}")

    lean = LEAN.read_text()
    chronos = CHRONOS.read_text()
    doc = DOC.read_text()
    artifact = json.loads(ARTIFACT.read_text())

    for token in FORBIDDEN_LEAN_TOKENS:
        if token in lean:
            raise SystemExit(f"forbidden Lean token present: {token}")

    for theorem in REQUIRED_THEOREMS:
        if f"theorem {theorem}" not in lean:
            raise SystemExit(f"missing theorem: {theorem}")

    for definition in REQUIRED_DEFS:
        if f"def {definition}" not in lean:
            raise SystemExit(f"missing definition: {definition}")

    if "import Chronos.Frontier.FiniteWitnessTheoremCluster" not in chronos:
        raise SystemExit("Chronos.lean does not import theorem cluster")

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in doc:
            raise SystemExit(f"missing boundary phrase: {phrase}")

    if artifact.get("status") != "PROVED_FINITE_THEOREM_CLUSTER_ONLY":
        raise SystemExit("artifact status mismatch")

    if artifact.get("lean_module") != "Chronos.Frontier.FiniteWitnessTheoremCluster":
        raise SystemExit("artifact Lean module mismatch")

    missing_theorems = set(REQUIRED_THEOREMS) - set(artifact.get("proved_theorems", []))
    if missing_theorems:
        raise SystemExit(f"artifact missing theorem names: {sorted(missing_theorems)}")

    missing_defs = set(REQUIRED_DEFS) - set(artifact.get("data_definitions", []))
    if missing_defs:
        raise SystemExit(f"artifact missing definition names: {sorted(missing_defs)}")

    print("Finite witness theorem cluster verified.")


if __name__ == "__main__":
    main()
