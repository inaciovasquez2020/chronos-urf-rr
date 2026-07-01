#!/usr/bin/env python3
import json
from pathlib import Path

TARGET = Path("Chronos/Frontier/H4_1_FGL_FinalSelectedInputClosure.lean")
ARTIFACT = Path("artifacts/external_validation/restricted_package_theorem_surface_boundary_2026_06_30.json")

def fail(message: str) -> None:
    raise SystemExit(f"INTERMEDIATE_ADMISSIBLE_CARRIER_DOMAIN_OPEN_GAP_FAIL := {message}")

def main() -> None:
    if not TARGET.exists():
        fail(f"missing Lean target {TARGET}")

    text = TARGET.read_text(encoding="utf-8")

    required_fragments = [
        "def H4_1_FGL_IsAdmissibleCarrier",
        "structure H4_1_FGL_IntermediateAdmissibleDomain where",
        "def intermediate_admissible_carrier_domain_closed : Prop :=",
        "theorem intermediate_admissible_carrier_domain_target_named :",
        "structure H4_1_FGL_IntermediateAdmissibleSeparatingObservableInput : Prop where",
        "theorem unrestricted_h4_1_fgl_promotion_refuted :",
    ]

    for fragment in required_fragments:
        if fragment not in text:
            fail(f"missing Lean fragment: {fragment}")

    forbidden_fragments = [
        "theorem intermediate_admissible_carrier_domain_closed_proof",
        "theorem intermediate_admissible_carrier_domain_proven",
        "theorem unrestricted_h4_1_fgl_closed_proof",
        "theorem unrestricted_h4_1_fgl_proven",
    ]

    for fragment in forbidden_fragments:
        if fragment in text:
            fail(f"forbidden affirmative closure fragment found: {fragment}")

    if not ARTIFACT.exists():
        fail(f"missing artifact {ARTIFACT}")

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    if data.get("unrestricted_domain_status") != "REFUTED_OPEN_GAP":
        fail("unrestricted_domain_status must remain REFUTED_OPEN_GAP")

    if data.get("intermediate_domain_status") != "OPEN_GAP":
        fail("intermediate_domain_status must be OPEN_GAP")

    print("INTERMEDIATE_ADMISSIBLE_CARRIER_DOMAIN_OPEN_GAP_OK")

if __name__ == "__main__":
    main()
