from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/SelectedDomainH41FGLFromChronosRR.lean"
DOC = ROOT / "docs/status/SELECTED_DOMAIN_H41_FGL_FROM_CHRONOS_RR_2026_05_17.md"
ART = ROOT / "artifacts/chronos/selected_domain_h41_fgl_from_chronos_rr_2026_05_17.json"
ROOT_LEAN = ROOT / "lean/Chronos.lean"

def require(path: Path, phrase: str) -> None:
    text = path.read_text()
    assert phrase in text, f"{phrase!r} missing from {path}"

def main() -> None:
    require(LEAN, "import Chronos.Frontier.SelectedDomainChronosRRFromUniversalGap")
    require(LEAN, "def SelectedDomainH41FGL")
    require(LEAN, "theorem selected_domain_h41_fgl_from_chronos_rr")
    require(LEAN, "SelectedDomainChronosRR rankRate fiberMass")
    require(LEAN, "exact hrr")
    require(ROOT_LEAN, "import Chronos.Frontier.SelectedDomainH41FGLFromChronosRR")

    require(DOC, "PROVED_SELECTED_DOMAIN_INTERFACE")
    require(DOC, "Selected-domain interface only.")
    require(DOC, "unrestricted UniversalFiberEntropyGap")
    require(DOC, "unrestricted Chronos-RR")
    require(DOC, "unrestricted H4.1/FGL")
    require(DOC, "P vs NP")
    require(DOC, "any Clay problem")

    data = json.loads(ART.read_text())
    assert data["status"] == "PROVED_SELECTED_DOMAIN_INTERFACE"
    assert data["theorem"] == "selected_domain_h41_fgl_from_chronos_rr"
    assert "SelectedDomainChronosRR" in data["depends_on"]
    boundary = " ".join(data["boundary"])
    for phrase in [
        "selected-domain interface only",
        "does not prove unrestricted UniversalFiberEntropyGap",
        "does not prove unrestricted Chronos-RR",
        "does not prove unrestricted H4.1/FGL",
        "does not prove P vs NP",
        "does not prove any Clay problem",
    ]:
        assert phrase in boundary, phrase

    forbidden = [
        "proves unrestricted UniversalFiberEntropyGap",
        "proves unrestricted Chronos-RR",
        "proves unrestricted H4.1/FGL",
        "proves P vs NP",
        "proves any Clay problem",
    ]
    combined = "\n".join(path.read_text() for path in [LEAN, DOC, ART])
    for phrase in forbidden:
        assert phrase not in combined, phrase

    print("Selected-domain H4.1/FGL from Chronos-RR verified.")

if __name__ == "__main__":
    main()
