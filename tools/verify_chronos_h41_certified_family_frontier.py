from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "chronos" / "Frontier" / "H41CertifiedFamily.lean"
DOC = ROOT / "docs" / "status" / "CHRONOS_H41_CERTIFIED_FAMILY_FRONTIER_2026_05_05.md"
ART = ROOT / "artifacts" / "chronos" / "h41_certified_family_frontier_2026_05_05.json"

required_lean = [
    "opaque CertifiedBoundedDegreeFOkLocalObstructionFamily",
    "noncomputable def Fn",
    "theorem Fn_certified",
    "noncomputable def mu_n",
    "axiom SearchFn",
    "axiom H41_LocalIndistinguishability",
    "theorem H41_constant_bound_explicit",
    "def h41_c_den",
    "RevealedBits τ * h41_c_den k Δ r < n",
]

required_doc = [
    "Status: FRONTIER_OPEN",
    "Closure: AXIOMATIC_FRONTIER_ONLY",
    "This does not prove H4.1.",
    "This does not prove Chronos theorem-level closure.",
    "This does not prove H4.1/FGL closure.",
    "This does not prove P vs NP.",
]

for path in [LEAN, DOC, ART]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = LEAN.read_text()
doc_text = DOC.read_text()
artifact = json.loads(ART.read_text())

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in required_doc:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

if artifact.get("status") != "FRONTIER_OPEN":
    raise SystemExit("artifact status must remain FRONTIER_OPEN")

if artifact.get("closure") != "AXIOMATIC_FRONTIER_ONLY":
    raise SystemExit("artifact closure must remain AXIOMATIC_FRONTIER_ONLY")

for forbidden in [
    "H4.1 proved",
    "Chronos closed",
    "P vs NP solved",
    "FGL closed"
]:
    if forbidden in lean_text or forbidden in doc_text or forbidden in json.dumps(artifact):
        raise SystemExit(f"forbidden overclaim token present: {forbidden}")

print("Chronos H4.1 certified family frontier verified: AXIOMATIC_FRONTIER_ONLY")
