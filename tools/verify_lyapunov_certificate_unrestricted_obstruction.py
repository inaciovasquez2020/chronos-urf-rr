#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/LyapunovCertificateUnrestrictedObstruction.lean"
ART = ROOT / "artifacts/chronos/lyapunov_certificate_unrestricted_obstruction_2026_05_17.json"
DOC = ROOT / "docs/status/LYAPUNOV_CERTIFICATE_UNRESTRICTED_OBSTRUCTION_2026_05_17.md"

REQUIRED = [
    "def zeroBoundSystem",
    "theorem no_LyapunovFiberBoundData_zeroBoundSystem",
    "theorem unrestricted_LyapunovFiberBoundData_false",
    "theorem unrestricted_LyapunovFiberBoundCertificate_false",
    "restricted admissible domain excluding zero-gap systems",
]

FORBIDDEN = [
    "proves P vs NP",
    "proves H4.1/FGL",
    "proves Chronos-RR",
    "proves any Clay problem",
    "unrestricted UniversalFiberEntropyGap proved",
    "unrestricted RateThickFiberCoercivity proved",
    "restricted admissible replacement domain constructed",
]

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

def main() -> None:
    lean = LEAN.read_text()
    doc = DOC.read_text()
    art = json.loads(ART.read_text())

    blob = lean + "\n" + doc + "\n" + json.dumps(art)

    for token in REQUIRED:
        require(token in blob, f"missing token: {token}")

    for token in FORBIDDEN:
        require(token not in blob, f"forbidden overclaim token: {token}")

    require(
        art["status"] == "UNRESTRICTED_LYAPUNOV_CERTIFICATE_FALSE",
        "bad artifact status",
    )
    require(art["counterexample"] == "zeroBoundSystem", "bad counterexample")
    require(art["theorem_promotion"] is False, "theorem promotion must be false")

    if shutil.which("lake") is not None:
        subprocess.run(
            ["lake", "build", "Chronos.Frontier.LyapunovCertificateUnrestrictedObstruction"],
            cwd=ROOT,
            check=True,
        )

    print("Lyapunov certificate unrestricted obstruction verified.")

if __name__ == "__main__":
    main()
