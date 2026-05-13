from pathlib import Path
import json
import re

LEAN = Path("Chronos/Frontier/UnrestrictedChronosRRObstructionRegistry.lean")
ARTIFACT = Path("artifacts/chronos/unrestricted_chronos_rr_obstruction_registry_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_UNRESTRICTED_RR_OBSTRUCTION_REGISTRY_2026_05_13.md")
ROOT = Path("Chronos.lean")

REQUIRED_LEAN = [
    "import Chronos.Frontier.ChronosRRRepositoryNativeConditionalClosure",
    "inductive UnrestrictedChronosRRObstruction",
    "missingUnrestrictedDepthBridge",
    "missingUnrestrictedUniversalFiberEntropyGap",
    "missingSemanticRankRateToFiberEntropySoundness",
    "repositoryNativeOnly",
    "def unrestrictedChronosRRObstructionRegistry",
    "theorem unrestricted_chronos_rr_obstruction_registry_nonempty",
    "theorem repository_native_conditional_closure_has_remaining_unrestricted_obstruction",
    "theorem canonical_repository_native_conditional_closure_has_remaining_unrestricted_obstruction"
]

REQUIRED_DOC = [
    "Status: UNRESTRICTED_CHRONOS_RR_OBSTRUCTION_REGISTRY_LOCKED",
    "missingUnrestrictedDepthBridge",
    "missingUnrestrictedUniversalFiberEntropyGap",
    "missingSemanticRankRateToFiberEntropySoundness",
    "repositoryNativeOnly",
    "Does not prove unrestricted Chronos-RR closure.",
    "Does not prove unrestricted DepthBridge.",
    "Does not prove unrestricted UniversalFiberEntropyGap.",
    "Does not prove SemanticRankRateToFiberEntropySoundness.",
    "Does not prove H4.1/FGL closure.",
    "Does not prove P vs NP closure.",
    "Does not prove any Clay-problem closure."
]

def require(path: Path) -> str:
    assert path.exists(), f"missing {path}"
    return path.read_text()

def main() -> None:
    lean = require(LEAN)
    doc = require(DOC)
    root = require(ROOT)
    data = json.loads(require(ARTIFACT))

    for token in REQUIRED_LEAN:
        assert token in lean, f"missing Lean token: {token}"

    for token in REQUIRED_DOC:
        assert token in doc, f"missing doc token: {token}"

    assert "import Chronos.Frontier.UnrestrictedChronosRRObstructionRegistry" in root

    assert data["status"] == "UNRESTRICTED_CHRONOS_RR_OBSTRUCTION_REGISTRY_LOCKED"
    assert data["registry"] == "unrestrictedChronosRRObstructionRegistry"
    assert data["main_theorem"] == "repository_native_conditional_closure_has_remaining_unrestricted_obstruction"
    assert data["dependency"] == "repository_native_chronos_rr_conditional_closure_from_depth_bridge"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False
    assert len(data["obstructions"]) == 4

    for pattern in [r"\baxiom\b", r"\badmit\b", r"\bsorry\b"]:
        assert re.search(pattern, lean) is None, f"forbidden Lean token: {pattern}"

    print("Unrestricted Chronos-RR obstruction registry verified.")

if __name__ == "__main__":
    main()
