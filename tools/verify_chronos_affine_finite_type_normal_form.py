from pathlib import Path

lean = Path("Chronos/Frontier/AffineFiniteTypeNormalForm.lean")
doc = Path("docs/status/CHRONOS_AFFINE_FINITE_TYPE_NORMAL_FORM_2026_05_05.md")

assert lean.exists(), "missing Lean normal-form file"
assert doc.exists(), "missing status doc"

lean_text = lean.read_text()
doc_text = doc.read_text()

required_lean = [
    "structure ChronosSkeleton",
    "def ChronosCons",
    "S.amul W = S.b",
    "structure ChronosCertificate",
    "def ChronosCertificateOfWitness",
    "def ChronosEmbedding",
    "structure FiniteLocalType",
    "structure ChronosOneStepData",
    "factor :",
    "theorem one_step_factorization",
    "structure AffineFiniteTypeNormalForm",
    "affine_finite_type_normal_form_is_structural_only",
]

required_doc = [
    "Status: STRUCTURAL_LOCALIZATION_ONLY",
    "Theorem closure: false",
    "FRONTIER_OPEN: true",
    "does not prove Chronos ED lower bounds",
    "does not prove",
    "P vs NP closure",
    "Remaining theorem-level obligations",
]

for needle in required_lean:
    assert needle in lean_text, f"missing Lean token: {needle}"

for needle in required_doc:
    assert needle in doc_text, f"missing doc token: {needle}"

for forbidden in [
    "solves P vs NP",
    "proves P vs NP",
    "Chronos theorem closed",
    "H4.1 closed",
    "FGL closed",
    "theorem-level closure: true",
    "Theorem closure: true",
]:
    assert forbidden not in lean_text
    assert forbidden not in doc_text

print("Chronos affine finite-type normal form verified: STRUCTURAL_LOCALIZATION_ONLY")
