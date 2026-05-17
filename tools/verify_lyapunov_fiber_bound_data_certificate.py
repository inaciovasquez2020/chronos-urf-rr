#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/LyapunovFiberBoundDataCertificate.lean"
ART = ROOT / "artifacts/chronos/lyapunov_fiber_bound_data_certificate_2026_05_17.json"
DOC = ROOT / "docs/status/LYAPUNOV_FIBER_BOUND_DATA_CERTIFICATE_2026_05_17.md"

REQUIRED = [
    "structure LyapunovFiberBoundCertificate",
    "theorem LyapunovFiberBoundData_from_certificate",
    "theorem exists_LB_LyapunovFiberBoundData_from_certificate",
    "theorem LyapunovFiberUniformFloor_from_certificate",
    "theorem NaturalHyperbolicBoundUniversalGap_from_certificate",
    "expansion_lower",
    "loss_upper",
    "entropy_controls_loss",
    "gap_pos",
]

FORBIDDEN = [
    "proves P vs NP",
    "proves H4.1/FGL",
    "proves Chronos-RR",
    "proves any Clay problem",
    "unrestricted UniversalFiberEntropyGap proved",
    "unrestricted RateThickFiberCoercivity proved",
    "unrestricted analytic certificate construction proved",
]

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

def main() -> None:
    lean = LEAN.read_text()
    doc = DOC.read_text()
    art = json.loads(ART.read_text())

    for token in REQUIRED:
        require(token in lean, f"missing Lean token: {token}")

    blob = lean + "\n" + doc + "\n" + json.dumps(art)
    for token in FORBIDDEN:
        require(token not in blob, f"forbidden overclaim token: {token}")

    require(
        art["status"] == "LYAPUNOV_FIBER_BOUND_DATA_CERTIFICATE_CLOSED",
        "bad artifact status",
    )
    require(art["theorem_promotion"] is False, "theorem promotion must be false")
    require(
        art["main_theorem"] == "LyapunovFiberBoundData_from_certificate",
        "bad main theorem",
    )

    if shutil.which("lake") is not None:
        subprocess.run(
            ["lake", "build", "Chronos.Frontier.LyapunovFiberBoundDataCertificate"],
            cwd=ROOT,
            check=True,
        )

    print("Lyapunov fiber-bound data certificate verified.")

if __name__ == "__main__":
    main()
