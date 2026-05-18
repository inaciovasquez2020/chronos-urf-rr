import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_selected_domain_admissible_embedding_construction_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_selected_domain_admissible_embedding_construction.py"],
        cwd=ROOT,
        check=True,
    )

def test_selected_domain_admissible_embedding_artifact_status() -> None:
    artifact = json.loads(
        (ROOT / "artifacts/chronos/selected_domain_admissible_embedding_construction_2026_05_18.json").read_text()
    )
    assert artifact["status"] == "SELECTED_DOMAIN_ADMISSIBLE_EMBEDDING_CONSTRUCTED"

def test_selected_domain_admissible_embedding_is_constructed_not_opaque_false() -> None:
    lean = (ROOT / "lean/Chronos/Frontier/SelectedDomainH41FGLToAdmissibleH41FGL.lean").read_text()
    assert "opaque AdmissibleH41FGL : Prop := False" not in lean
    assert "selected_domain_admissible_h41_fgl_identity_embedding" in lean
    assert "fun hSelected => hSelected" in lean
