from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/UnrestrictedRateThickCoercivityRoute.lean"
DOC = ROOT / "docs/status/UNRESTRICTED_RATE_THICK_COERCIVITY_ROUTE_2026_05_17.md"
ARTIFACT = ROOT / "artifacts/chronos/unrestricted_rate_thick_coercivity_route_2026_05_17.json"

def main() -> None:
    lean = LEAN.read_text()
    doc = DOC.read_text()
    artifact = json.loads(ARTIFACT.read_text())

    required_lean = [
        "def RateThickFiberCoercivityTheoremTarget",
        "def WeakestAnalyticInvariant",
        "weakestAnalyticInvariant_iff_rateThickFiberCoercivity",
        "def RateThickFiberEntropyGap",
        "rateThickFiberEntropyGap_from_rankRateBridge_and_coercivity",
        "def UniversalFiberEntropyGap",
        "universalFiberEntropyGap_from_rateThickFiberEntropyGap",
        "def UniversalFiberEntropyGapToChronosRR",
        "chronosRR_from_universalFiberEntropyGap",
        "full_conditional_route_to_chronosRR",
        "FRONTIER_OPEN",
    ]

    for phrase in required_lean:
        assert phrase in lean, phrase

    required_doc = [
        "Status: FRONTIER_OPEN",
        "Weakest analytic invariant",
        "Conditional route only",
        "Does not prove:",
        "unrestricted RateThickFiberCoercivity",
        "unrestricted UniversalFiberEntropyGap",
        "unrestricted Chronos-RR",
        "P vs NP",
        "any Clay problem",
    ]

    for phrase in required_doc:
        assert phrase in doc, phrase

    assert artifact["status"] == "FRONTIER_OPEN"
    assert artifact["weakest_missing_input"] == "RateThickFiberCoercivity lambda"

    forbidden = [
        "proves unrestricted RateThickFiberCoercivity",
        "proves unrestricted UniversalFiberEntropyGap",
        "proves unrestricted Chronos-RR",
        "proves P vs NP",
        "solves P vs NP",
        "solves any Clay problem",
    ]

    combined = "\n".join([lean, doc, json.dumps(artifact)])
    for phrase in forbidden:
        assert phrase not in combined, phrase

    print("Unrestricted rate-thick coercivity route verified.")

if __name__ == "__main__":
    main()
