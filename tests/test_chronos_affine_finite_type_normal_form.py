from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_affine_finite_type_files_exist():
    assert (ROOT / "Chronos/Frontier/AffineFiniteTypeNormalForm.lean").exists()
    assert (ROOT / "docs/status/CHRONOS_AFFINE_FINITE_TYPE_NORMAL_FORM_2026_05_05.md").exists()
    assert (ROOT / "tools/verify_chronos_affine_finite_type_normal_form.py").exists()

def test_affine_finite_type_boundary_language():
    text = (ROOT / "docs/status/CHRONOS_AFFINE_FINITE_TYPE_NORMAL_FORM_2026_05_05.md").read_text()
    assert "STRUCTURAL_LOCALIZATION_ONLY" in text
    assert "Theorem closure: false" in text
    assert "FRONTIER_OPEN: true" in text
    assert "P vs NP closure" in text

def test_affine_finite_type_lean_surface():
    text = (ROOT / "Chronos/Frontier/AffineFiniteTypeNormalForm.lean").read_text()
    assert "structure ChronosSkeleton" in text
    assert "def ChronosCons" in text
    assert "S.amul W = S.b" in text
    assert "structure FiniteLocalType" in text
    assert "structure ChronosOneStepData" in text
    assert "theorem one_step_factorization" in text
    assert "structure AffineFiniteTypeNormalForm" in text
