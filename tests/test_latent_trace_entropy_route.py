import subprocess
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_latent_trace_entropy_route_verifier_passes() -> None:
    subprocess.run(
        ["python3", "tools/verify_latent_trace_entropy_route.py"],
        cwd=ROOT,
        check=True,
    )

def test_latent_trace_entropy_route_has_no_sorry() -> None:
    lean = (ROOT / "lean/Chronos/Frontier/LatentTraceEntropyRoute.lean").read_text()
    assert "sorry" not in lean
    assert "admit" not in lean
    assert "axiom " not in lean

def test_latent_trace_entropy_route_boundary_present() -> None:
    doc = (ROOT / "docs/status/LATENT_TRACE_ENTROPY_ROUTE_2026_05_17.md").read_text()
    assert "Does not prove:" in doc
    assert "unrestricted UniversalFiberEntropyGap" in doc
    assert "P vs NP" in doc

def test_rate_thick_fiber_coercivity_refutation_present() -> None:
    lean = (ROOT / "lean/Chronos/Frontier/LatentTraceEntropyRoute.lean").read_text()
    doc = (ROOT / "docs/status/LATENT_TRACE_ENTROPY_ROUTE_2026_05_17.md").read_text()
    assert "theorem rateThickFiberCoercivity_refuted" in lean
    assert "¬ RateThickFiberCoercivity lam" in lean
    assert "PositiveEntropyAdmissibleClass" in doc

def test_positive_entropy_admissible_class_bridge_present() -> None:
    lean = (ROOT / "lean/Chronos/Frontier/LatentTraceEntropyRoute.lean").read_text()
    doc = (ROOT / "docs/status/LATENT_TRACE_ENTROPY_ROUTE_2026_05_17.md").read_text()
    artifact = json.loads((ROOT / "artifacts/chronos/latent_trace_entropy_route_2026_05_17.json").read_text())
    assert "def PositiveEntropyAdmissibleClass" in lean
    assert "theorem rateThickFiberCoercivity_from_positiveEntropyAdmissibleClass" in lean
    assert "This is a conditional repair bridge only" in doc
    assert "PositiveEntropyAdmissibleClass" in artifact["closed_surfaces"]
    assert "rateThickFiberCoercivity_from_positiveEntropyAdmissibleClass" in artifact["closed_surfaces"]
    assert "PositiveEntropyAdmissibleClassUniformWitness" in artifact["frontier_inputs"]

def test_positive_entropy_uniform_witness_interface_present() -> None: import json; lean = (ROOT / "lean/Chronos/Frontier/LatentTraceEntropyRoute.lean").read_text(); doc = (ROOT / "docs/status/LATENT_TRACE_ENTROPY_ROUTE_2026_05_17.md").read_text(); artifact = json.loads((ROOT / "artifacts/chronos/latent_trace_entropy_route_2026_05_17.json").read_text()); assert "structure PositiveEntropyAdmissibleClassUniformWitness" in lean; assert "theorem rateThickFiberCoercivity_from_positiveEntropyAdmissibleClassUniformWitness" in lean; assert "This is interface closure only" in doc; assert "PositiveEntropyAdmissibleClassUniformWitness" in artifact["closed_surfaces"]; assert "rateThickFiberCoercivity_from_positiveEntropyAdmissibleClassUniformWitness" in artifact["closed_surfaces"]; assert "PositiveEntropyAdmissibleClassUniformWitnessConstruction" in artifact["frontier_inputs"]
