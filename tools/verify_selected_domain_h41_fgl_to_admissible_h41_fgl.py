from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/SelectedDomainH41FGLToAdmissibleH41FGL.lean"
DOC = ROOT / "docs/status/SELECTED_DOMAIN_H41_FGL_TO_ADMISSIBLE_H41_FGL_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/selected_domain_h41_fgl_to_admissible_h41_fgl_2026_05_18.json"


def main() -> None:
    lean = LEAN.read_text()
    doc = DOC.read_text()
    artifact_text = ARTIFACT.read_text()
    artifact = json.loads(artifact_text)

    assert (
        "def AdmissibleH41FGL" in lean
        and "SelectedDomainH41FGL" in lean
    ), "AdmissibleH41FGL must be defined by selected-domain transport"

    assert "opaque AdmissibleH41FGL : Prop := False" not in lean
    assert "structure SelectedDomainAdmissibleH41FGLEmbedding" in lean
    assert "to_admissible :" in lean
    assert "SelectedDomainH41FGL" in lean
    assert "AdmissibleH41FGL" in lean
    assert (
        "to_admissible" in lean
        or "selected_domain_h41_fgl_to_admissible_h41_fgl" in lean
        or "admissible_h41_fgl_from_selected_domain_h41_fgl" in lean
    ), "missing selected-domain to admissible transport map"
    assert "theorem admissible_h41_fgl_from_selected_domain_h41_fgl" in lean
    assert "exact hEmbed.to_admissible hSelected" in lean

    assert artifact["status"] == "SELECTED_DOMAIN_H41_FGL_TO_ADMISSIBLE_H41_FGL_CLOSED"
    assert "selected-domain to admissible bridge only" in doc
    assert "requires explicit admissible embedding data" in doc
    assert "does not construct the embedding" in doc
    assert "does not prove unrestricted H4.1/FGL" in doc
    assert "does not prove P vs NP" in doc
    assert "does not prove any Clay problem" in doc
    assert "No admissible unrestricted step." in doc

    forbidden = [
        "admit",
        "sorry",
        "axiom",
        "proves unrestricted H4.1/FGL",
        "proves P vs NP",
        "proves any Clay problem",
        "constructs the embedding",
    ]
    combined = lean + "\n" + doc + "\n" + artifact_text
    for token in forbidden:
        assert token not in combined

    print("Selected-domain H4.1/FGL to admissible H4.1/FGL bridge verified.")


if __name__ == "__main__":
    main()
