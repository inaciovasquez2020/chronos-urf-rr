#!/usr/bin/env python3
from pathlib import Path
import sys

LEAN = Path("lean/Chronos/Frontier/LocalAnisotropicTurnaroundObservationReceipt.lean")
FRONTIER = Path("lean/Chronos/Frontier.lean")
WORKFLOW = Path(".github/workflows/external-status-lock.yml")

REQUIRED = [
    "import Chronos.Frontier.LocalAnisotropicTurnaroundInputSurface",
    "structure LocalAnisotropicTurnaroundObservationReceipt : Type where",
    'sourceTitle := "The Hubble flow around the Local Group"',
    'sourceAuthors := "I. D. Karachentsev, O. G. Kashibadze, D. I. Makarov, R. B. Tully"',
    'sourceArxivId := "0811.4610"',
    'sourceDoi := "10.1111/j.1365-2966.2008.14300.x"',
    "sampleGalaxyCount := 30",
    "distanceLowerMpcX10 := 7",
    "distanceUpperMpcX10 := 30",
    "localHubbleKmSPerMpc := localAnisotropicTurnaroundReceiptLocalHubbleKmSPerMpc",
    "peculiarVelocityDispersionKmS := localAnisotropicTurnaroundReceiptPeculiarVelocityResidualKmS",
    "zeroVelocityRadiusMpcX100 := localAnisotropicTurnaroundReceiptR0MpcX100",
    "radialVelocityErrorKmS := 4",
    "distanceErrorVelocityEquivalentKmS := 10",
    "theorem local_anisotropic_turnaround_observation_receipt_matches_input_constants",
    "theorem local_anisotropic_turnaround_observation_receipt_is_boundary_only",
]

FORBIDDEN = [
    "gravity_closure",
    "Einstein_limit",
    "new_cosmology_solution",
    "turnaround_radius_proves_gravity",
    "proves_gravity",
    "derives_Einstein",
    "solves_cosmology",
]


def fail(msg: str) -> None:
    print(f"LOCAL_ANISOTROPIC_TURNAROUND_OBSERVATION_RECEIPT_FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not LEAN.exists():
        fail(f"missing {LEAN}")

    text = LEAN.read_text(encoding="utf-8")

    for needle in REQUIRED:
        if needle not in text:
            fail(f"missing required receipt token: {needle}")

    for forbidden in FORBIDDEN:
        if forbidden in text:
            fail(f"forbidden overclaim token present: {forbidden}")

    if "axiom " in text or "opaque " in text or "sorry" in text or "admit" in text:
        fail("forbidden Lean escape hatch present")

    if FRONTIER.exists():
        frontier = FRONTIER.read_text(encoding="utf-8")
        expected_import = "import Chronos.Frontier.LocalAnisotropicTurnaroundObservationReceipt"
        if expected_import not in frontier:
            fail("receipt import missing from Chronos.Frontier")

    if WORKFLOW.exists():
        workflow = WORKFLOW.read_text(encoding="utf-8")
        expected_cmd = "python3 tools/verifier/verify_local_anisotropic_turnaround_observation_receipt.py"
        if expected_cmd not in workflow:
            fail("receipt verifier not wired into external-status-lock workflow")

    print("LOCAL_ANISOTROPIC_TURNAROUND_OBSERVATION_RECEIPT_OK")


if __name__ == "__main__":
    main()
