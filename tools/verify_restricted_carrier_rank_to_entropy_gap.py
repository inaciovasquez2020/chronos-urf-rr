from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/RestrictedCarrierRankToEntropyGap.lean"
DOC = ROOT / "docs/status/RESTRICTED_CARRIER_RANK_TO_ENTROPY_GAP_2026_05_17.md"
ART = ROOT / "artifacts/chronos/restricted_carrier_rank_to_entropy_gap_2026_05_17.json"
ROOT_LEAN = ROOT / "lean/Chronos.lean"

def require(path: Path, phrase: str) -> None:
    text = path.read_text()
    assert phrase in text, f"{phrase!r} missing from {path}"

def main() -> None:
    require(LEAN, "theorem restricted_carrier_rank_to_entropy_gap")
    require(LEAN, "RestrictedCarrierFiberEntropyGap rankRate fiberMass")
    require(LEAN, "exact hcoercive X h_rank")
    require(ROOT_LEAN, "import Chronos.Frontier.RestrictedCarrierRankToEntropyGap")

    require(DOC, "PROVED_RESTRICTED_BRIDGE")
    require(DOC, "Restricted carrier bridge only.")
    require(DOC, "Does not prove:")
    require(DOC, "unrestricted UniversalFiberEntropyGap")
    require(DOC, "P vs NP")
    require(DOC, "any Clay problem")

    data = json.loads(ART.read_text())
    assert data["status"] == "PROVED_RESTRICTED_BRIDGE"
    assert data["theorem"] == "restricted_carrier_rank_to_entropy_gap"
    boundary = " ".join(data["boundary"])
    for phrase in [
        "restricted carrier bridge only",
        "does not prove unrestricted UniversalFiberEntropyGap",
        "does not prove unrestricted Chronos-RR",
        "does not prove P vs NP",
        "does not prove any Clay problem",
    ]:
        assert phrase in boundary, phrase

    forbidden = [
        "proves unrestricted UniversalFiberEntropyGap",
        "proves unrestricted Chronos-RR",
        "proves H4.1/FGL",
        "proves P vs NP",
        "proves any Clay problem",
    ]
    combined = "\n".join(path.read_text() for path in [LEAN, DOC, ART])
    for phrase in forbidden:
        assert phrase not in combined, phrase

    print("Restricted carrier rank-to-entropy-gap bridge verified.")

if __name__ == "__main__":
    main()
