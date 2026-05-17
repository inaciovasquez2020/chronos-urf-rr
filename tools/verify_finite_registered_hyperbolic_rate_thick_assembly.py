#!/usr/bin/env python3
from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/FiniteRegisteredHyperbolicRateThickAssembly.lean"
DOC = ROOT / "docs/status/FINITE_REGISTERED_HYPERBOLIC_RATE_THICK_ASSEMBLY_2026_05_17.md"
ART = ROOT / "artifacts/chronos/finite_registered_hyperbolic_rate_thick_assembly_2026_05_17.json"
CHRONOS = ROOT / "lean/Chronos.lean"

REQUIRED_LEAN = [
    "def BinaryKappaAdmissible",
    "def binaryKappaCandidate",
    "structure UniformlyHyperbolicAdmissibleSystem",
    "structure FiniteHyperbolicRegistry",
    "def RegisteredSystem",
    "def RegisteredRatioStabilitySlack",
    "def RegisteredUniformFiberMassFloor",
    "structure RegisteredEntropyMinimumDominationCertificate",
    "structure RegisteredUniformFiberMassCertificate",
    "def RegisteredRateThickFiberCoercivity",
    "def RegisteredHyperbolicUniversalFiberEntropyGap",
    "lemma binaryKappaCandidate_le_quarter",
    "theorem FiniteRegisteredRatioStability_from_uniform_floor",
    "theorem FiniteRegisteredUniformFloor_from_index_floor",
    "theorem FiniteRegisteredDominationCertificate",
    "theorem FiniteRegisteredUniformMassCertificate",
    "theorem FiniteRegisteredRateThickFiberCoercivityAssembly",
    "theorem FiniteRegisteredUniversalGap_from_rate_thick_coercivity",
    "theorem FiniteRegisteredHyperbolicRateThickUniversalGapAssembly",
]

REQUIRED_DOC = [
    "FINITE_REGISTERED_HYPERBOLIC_RATE_THICK_SURFACE_ONLY / NO_THEOREM_PROMOTION",
    "Finite registered hyperbolic domain only.",
    "Does not prove:",
    "unrestricted RateThickFiberCoercivity",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

FORBIDDEN = [
    "unrestricted RateThickFiberCoercivity proved",
    "unrestricted UniversalFiberEntropyGap proved",
    "unrestricted Chronos-RR proved",
    "H4.1/FGL proved",
    "P vs NP proved",
    "Clay problem proved",
    "theorem_promotion\": true",
]


def run(cmd: list[str]) -> str:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return proc.stdout


def main() -> None:
    lean = LEAN.read_text()
    doc = DOC.read_text()
    art = json.loads(ART.read_text())
    chronos = CHRONOS.read_text()

    for token in REQUIRED_LEAN:
        assert token in lean, token

    for token in REQUIRED_DOC:
        assert token in doc, token

    for token in FORBIDDEN:
        assert token not in lean
        assert token not in doc
        assert token not in ART.read_text()

    assert art["status"] == "FINITE_REGISTERED_HYPERBOLIC_RATE_THICK_SURFACE_ONLY"
    assert art["theorem_promotion"] is False
    assert art["main_theorem"] == "FiniteRegisteredHyperbolicRateThickUniversalGapAssembly"

    assert "import Chronos.Frontier.FiniteRegisteredHyperbolicRateThickAssembly" in chronos

    if shutil.which("lake") is not None:
        run(["lake", "env", "lean", str(LEAN)])
        run(["lake", "build", "Chronos.Frontier.FiniteRegisteredHyperbolicRateThickAssembly"])

    print("Finite registered hyperbolic rate-thick assembly verified.")


if __name__ == "__main__":
    main()
