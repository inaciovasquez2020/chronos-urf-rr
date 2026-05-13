import json
from pathlib import Path

LEAN = Path("Chronos/Frontier/UnrestrictedChronosRRObstructionRegistry.lean")
ARTIFACT = Path("artifacts/chronos/unrestricted_chronos_rr_obstruction_registry_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_UNRESTRICTED_RR_OBSTRUCTION_REGISTRY_2026_05_13.md")

def test_registry_inductive_exists():
    text = LEAN.read_text()
    assert "inductive UnrestrictedChronosRRObstruction" in text
    assert "missingUnrestrictedDepthBridge" in text
    assert "missingUnrestrictedUniversalFiberEntropyGap" in text
    assert "missingSemanticRankRateToFiberEntropySoundness" in text
    assert "repositoryNativeOnly" in text

def test_registry_nonempty_theorem_exists():
    text = LEAN.read_text()
    assert "def unrestrictedChronosRRObstructionRegistry" in text
    assert "theorem unrestricted_chronos_rr_obstruction_registry_nonempty" in text

def test_repository_native_conditional_has_remaining_obstruction():
    text = LEAN.read_text()
    assert "RepositoryNativeConditionalClosureHasRemainingUnrestrictedObstruction" in text
    assert "repository_native_conditional_closure_has_remaining_unrestricted_obstruction" in text
    assert "canonical_repository_native_conditional_closure_has_remaining_unrestricted_obstruction" in text

def test_no_axiom_admit_or_sorry():
    text = LEAN.read_text()
    assert "axiom" not in text
    assert "admit" not in text
    assert "sorry" not in text

def test_artifact_boundary():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "UNRESTRICTED_CHRONOS_RR_OBSTRUCTION_REGISTRY_LOCKED"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False
    assert data["obstructions"] == [
        "missingUnrestrictedDepthBridge",
        "missingUnrestrictedUniversalFiberEntropyGap",
        "missingSemanticRankRateToFiberEntropySoundness",
        "repositoryNativeOnly",
    ]
    boundary = "\n".join(data["boundary"])
    assert "Does not prove unrestricted Chronos-RR closure." in boundary
    assert "Does not prove P vs NP closure." in boundary

def test_status_doc_boundary():
    text = DOC.read_text()
    assert "Status: UNRESTRICTED_CHRONOS_RR_OBSTRUCTION_REGISTRY_LOCKED" in text
    assert "Does not prove unrestricted Chronos-RR closure." in text
    assert "Does not prove any Clay-problem closure." in text
