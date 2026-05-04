#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "artifacts/chronos/certificates/chronos_certificate_primitive_axiom_2026_05_04.json"
DOC = ROOT / "docs/status/CHRONOS_CERTIFICATE_PRIMITIVE_AXIOM_2026_05_04.md"

REQUIRED_TOKENS = [
    "CHRONOS_CERTIFICATE_PRIMITIVE_AXIOM",
    "AXIOMATIC_DECLARATION_ONLY",
    "CCPA_TERMINAL_PRIMITIVE",
    "T_CHR_TYPE_FAMILY_REQUIRED",
    "FINTYPE_REQUIRED",
    "NONEMPTY_REQUIRED",
    "DECIDABLE_EQ_REQUIRED",
    "TARGET_SIDE_INDEPENDENT",
    "THEOREM_CLOSURE_FALSE",
    "CHRONOS_CLOSURE_FALSE",
    "H4_1_FGL_CLOSURE_FALSE",
    "P_VS_NP_CLAIM_FALSE",
    "NO_CERTIFICATE_EMBEDDING_CLAIM",
]

FORBIDDEN = [
    "THEOREM_CLOSURE_TRUE",
    "CHRONOS_CLOSURE_TRUE",
    "H4_1_FGL_CLOSURE_TRUE",
    "P_VS_NP_CLAIM_TRUE",
    "CHRONOS_SOLVED",
    "H4_1_SOLVED",
    "FGL_SOLVED",
    "CERTIFICATE_EMBEDDING_PROVED",
    "CCSL_PROVED",
    "ENTROPY_BRIDGE_PROVED",
]

def main() -> None:
    if not CERT.exists():
        raise SystemExit(f"missing certificate: {CERT}")
    if not DOC.exists():
        raise SystemExit(f"missing status doc: {DOC}")

    data = json.loads(CERT.read_text(encoding="utf-8"))
    text = DOC.read_text(encoding="utf-8")
    combined = text + "\n" + json.dumps(data, sort_keys=True)

    if data.get("status") != "AXIOMATIC_DECLARATION_ONLY":
        raise SystemExit("status must remain AXIOMATIC_DECLARATION_ONLY")
    if data.get("theorem_closure") is not False:
        raise SystemExit("theorem_closure must be false")
    if data.get("chronos_closure") is not False:
        raise SystemExit("chronos_closure must be false")
    if data.get("h4_1_fgl_closure") is not False:
        raise SystemExit("h4_1_fgl_closure must be false")
    if data.get("p_vs_np_closure") is not False:
        raise SystemExit("p_vs_np_closure must be false")
    if data.get("terminal_missing_primitive") != "CCPA":
        raise SystemExit("terminal_missing_primitive must be CCPA")
    if data.get("primitive_type_family") != "T_Chr : Nat -> Type":
        raise SystemExit("primitive_type_family mismatch")

    for required in [
        "Fintype(T_Chr n)",
        "Nonempty(T_Chr n)",
        "DecidableEq(T_Chr n)",
    ]:
        if required not in data.get("required_instances", []):
            raise SystemExit(f"missing required instance: {required}")

    for token in REQUIRED_TOKENS:
        if token not in text:
            raise SystemExit(f"missing token in doc: {token}")
        if token not in data.get("machine_tokens", []):
            raise SystemExit(f"missing token in json: {token}")

    for forbidden in FORBIDDEN:
        if forbidden in combined:
            raise SystemExit(f"forbidden overclaim detected: {forbidden}")

    print("Chronos certificate primitive axiom verified: AXIOMATIC_DECLARATION_ONLY")

if __name__ == "__main__":
    main()
