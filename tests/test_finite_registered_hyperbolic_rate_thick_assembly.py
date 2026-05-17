from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_status_doc_boundary():
    doc = (
        ROOT / "docs/status/FINITE_REGISTERED_HYPERBOLIC_RATE_THICK_ASSEMBLY_2026_05_17.md"
    ).read_text()
    assert "FINITE_REGISTERED_HYPERBOLIC_RATE_THICK_SURFACE_ONLY / NO_THEOREM_PROMOTION" in doc
    assert "Finite registered hyperbolic domain only." in doc
    assert "Does not prove:" in doc
    assert "unrestricted RateThickFiberCoercivity" in doc
    assert "unrestricted UniversalFiberEntropyGap" in doc
    assert "unrestricted Chronos-RR" in doc
    assert "H4.1/FGL" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc


def test_artifact_boundary():
    data = json.loads(
        (
            ROOT
            / "artifacts/chronos/finite_registered_hyperbolic_rate_thick_assembly_2026_05_17.json"
        ).read_text()
    )
    assert data["status"] == "FINITE_REGISTERED_HYPERBOLIC_RATE_THICK_SURFACE_ONLY"
    assert data["theorem_promotion"] is False
    assert data["main_theorem"] == "FiniteRegisteredHyperbolicRateThickUniversalGapAssembly"


def test_verifier_passes():
    subprocess.run(
        [sys.executable, "tools/verify_finite_registered_hyperbolic_rate_thick_assembly.py"],
        cwd=ROOT,
        check=True,
    )
