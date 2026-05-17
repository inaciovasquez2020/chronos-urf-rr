#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/LyapunovFiberBoundRoute.lean"
ART = ROOT / "artifacts/chronos/lyapunov_fiber_bound_route_2026_05_17.json"
DOC = ROOT / "docs/status/LYAPUNOV_FIBER_BOUND_ROUTE_2026_05_17.md"

REQUIRED = [
    "structure LyapunovFiberBoundData",
    "expansion_lower",
    "loss_upper",
    "gap_pos",
    "theorem LyapunovFiberUniformFloor_from_bounds",
    "theorem entropyMass_uniform_floor_from_bounds",
    "theorem NaturalHyperbolicBoundUniversalGap_from_lyapunov_bounds",
    "entropy_controls_loss",
]

FORBIDDEN = [
    "proves P vs NP",
    "proves H4.1/FGL",
    "proves Chronos-RR",
    "proves any Clay problem",
    "unrestricted UniversalFiberEntropyGap proved",
    "unrestricted RateThickFiberCoercivity proved",
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

    require(art["status"] == "LYAPUNOV_FIBER_BOUND_ROUTE_ONLY", "bad artifact status")
    require(art["theorem_promotion"] is False, "theorem promotion must be false")
    require(art["weakest_missing_input"] == "LyapunovFiberBoundData D L B", "bad weakest missing input")

    if shutil.which("lake") is not None:
        subprocess.run(
            ["lake", "build", "Chronos.Frontier.LyapunovFiberBoundRoute"],
            cwd=ROOT,
            check=True,
        )

    print("Lyapunov fiber-bound route verified.")

if __name__ == "__main__":
    main()
