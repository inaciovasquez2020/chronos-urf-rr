import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_universal_measure_fiber_mass_lemma_refutation_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_universal_measure_fiber_mass_lemma_refutation.py"],
        cwd=ROOT,
        check=True,
    )

def test_universal_measure_fiber_mass_lemma_refutation_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/universal_measure_fiber_mass_lemma_refutation_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "UNRESTRICTED_MEASURE_FIBER_MASS_LEMMA_REFUTED_RESTRICTED_TARGET_CLOSED"
    assert "UniversalWeakestMissingMeasureFiberMassLemma" in artifact["refuted"]
    assert "UnrestrictedRateThickFiberCoercivityTarget" in artifact["refuted"]
    boundary = "\n".join(artifact["boundary"])
    assert "does not prove unrestricted RateThickFiberCoercivity" in boundary
    assert "does not prove unrestricted UniversalFiberEntropyGap" in boundary
    assert "does not prove P vs NP" in boundary

def test_universal_measure_fiber_mass_lemma_refutation_lean_surface_has_no_sorry():
    lean = (ROOT / "lean/Chronos/Frontier/UniversalWeakestMissingMeasureFiberMassLemmaRefutation.lean").read_text()
    assert "theorem UniversalWeakestMissingMeasureFiberMassLemma_refuted" in lean
    assert "theorem UnrestrictedRateThickFiberCoercivityTarget_refuted" in lean
    assert "theorem RestrictedMeasureFiberMassFloorTarget_solved" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
