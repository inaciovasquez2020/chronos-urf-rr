from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "Chronos/Frontier/UniversalFiberEntropyGapNativeObligations.lean"
root = ROOT / "Chronos.lean"
doc = ROOT / "docs/status/CHRONOS_UNIVERSAL_FIBER_ENTROPY_GAP_NATIVE_OBLIGATIONS_2026_05_10.md"
artifact = ROOT / "artifacts/chronos/universal_fiber_entropy_gap_native_obligations_2026_05_10.json"

for path in [lean, root, doc, artifact]:
    assert path.exists(), f"missing required file: {path}"

lean_text = lean.read_text()
for token in [
    "RepositoryNativeCarrierFamily",
    "ChronosNativeCarrierFamily",
    "CertifiedRankRateLowerBound",
    "CertifiedFiberEntropyLowerBound",
    "RankRateGapNativeTheorem",
    "ChronosNativeRankRateGapTheorem",
    "CountingFiberSeparationTheorem",
    "FiberMassBalanceTheorem",
    "UniversalFiberEntropyGapTheorem",
    "RankRateGapToCountingFiberSeparation",
    "CountingFiberSeparationToFiberMassBalance",
    "FiberMassBalanceToUniversalFiberEntropyGap",
    "conditional_universal_fiber_entropy_gap_from_rank_rate_gap",
    "UniversalFiberEntropyGapTerminalObligation",
    "RankRateGapProofStillRequired",
]:
    assert token in lean_text, token

assert "import Chronos.Frontier.UniversalFiberEntropyGapNativeObligations" in root.read_text()

doc_text = doc.read_text()
for token in [
    "UNIVERSAL_FIBER_ENTROPY_GAP_CONDITIONAL_COMPOSITION_ONLY",
    "ChronosNativeRankRateGapTheorem",
    "Terminal missing theorem-level object",
    "does not assert",
    "UniversalFiberEntropyGap theorem closure",
    "P vs NP closure",
    "Clay-problem closure",
]:
    assert token in doc_text, token

data = json.loads(artifact.read_text())
assert data["status"] == "UNIVERSAL_FIBER_ENTROPY_GAP_CONDITIONAL_COMPOSITION_ONLY"
assert data["terminal_missing_object"] == "ChronosNativeRankRateGapTheorem"
assert data["boundary"]["rank_rate_gap_proved"] is False
assert data["boundary"]["universal_fiber_entropy_gap_closed"] is False
assert data["boundary"]["chronos_rr_theorem_closed"] is False
assert data["boundary"]["p_vs_np"] is False
assert data["boundary"]["clay_problem"] is False

for forbidden in [
    "solves P vs NP",
    "proves P vs NP",
    "resolves P vs NP",
    "solves the Clay",
    "resolves the Clay",
    "RankRateGap proved",
    "UniversalFiberEntropyGap theorem closed",
    "Chronos-RR theorem closed"
]:
    assert forbidden not in doc_text
    assert forbidden not in lean_text

print("UniversalFiberEntropyGap native obligations verified.")
