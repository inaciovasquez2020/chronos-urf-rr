from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/AdmissibleChronosRRToH41FGL.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/ADMISSIBLE_CHRONOS_RR_TO_H41_FGL_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/admissible_chronos_rr_to_h41_fgl_2026_05_18.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.AdmissibleUniversalFiberEntropyGapToChronosRR",
    "structure H41FGLTarget",
    "def ChronosRRToH41FGLBridge",
    "theorem h41FGLTarget_from_chronosRRTarget",
    "theorem ChronosRRToH41FGLBridge_solved",
    "def AdmissibleChronosRRToH41FGL",
    "theorem AdmissibleChronosRRToH41FGL_solved",
    "def AdmissibleH41FGLTarget",
    "theorem AdmissibleH41FGLTarget_solved",
    "def UnrestrictedH41FGLTarget",
    "theorem UnrestrictedH41FGLTarget_refuted",
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.AdmissibleChronosRRToH41FGL" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "ADMISSIBLE_H41_FGL_TARGET_CLOSED_RESTRICTED_ONLY",
    "unexpected artifact status",
)

required_boundary = [
    "does not prove unrestricted RateThickFiberCoercivity",
    "does not prove unrestricted UniversalFiberEntropyGap",
    "does not prove unrestricted Chronos-RR",
    "does not prove unrestricted H4.1/FGL",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]

for token in required_boundary:
    require(token in doc, f"missing doc boundary token: {token}")
    require(any(token in b for b in artifact["boundary"]), f"missing artifact boundary token: {token}")

for forbidden in [
    "proves unrestricted RateThickFiberCoercivity",
    "proves unrestricted UniversalFiberEntropyGap",
    "proves unrestricted Chronos-RR",
    "proves unrestricted H4.1/FGL",
    "proves P vs NP",
    "proves any Clay problem",
]:
    require(forbidden not in doc, f"forbidden overclaim in doc: {forbidden}")
    require(forbidden not in json.dumps(artifact), f"forbidden overclaim in artifact: {forbidden}")

print("Admissible Chronos-RR to H4.1/FGL verified.")
