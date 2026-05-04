#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "Chronos/Certificate/CPOLTypeGate.lean"
CERT = ROOT / "artifacts/chronos/certificates/chronos_cpol_type_gate_2026_05_04.json"
DOC = ROOT / "docs/status/CHRONOS_CPOL_TYPE_GATE_2026_05_04.md"

TOKENS = [
    "CHRONOS_CPOL_TYPE_GATE",
    "CPOL_TYPE_GATE_CLOSED_ONLY",
    "T_CHR_DEFINED",
    "T_CHR_SINGLETON_CARRIER",
    "NONEMPTY_PROVED",
    "DECIDABLE_EQ_PROVED",
    "CANONICAL_WITNESS_PROVED",
    "DECIDABLE_EQ_NONEMPTY_PROVED",
    "THEOREM_CLOSURE_FALSE",
    "CHRONOS_CLOSURE_FALSE",
    "H4_1_FGL_CLOSURE_FALSE",
    "P_VS_NP_CLAIM_FALSE",
    "NO_C_N_CHR_CONSTRUCTION",
    "NO_CPDL_CLAIM",
    "NO_CCSL_CLAIM",
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
    "CCSL_PROVED",
    "CPDL_PROVED",
    "CERTIFICATE_EMBEDDING_PROVED",
]

def main() -> None:
    for path in [LEAN, CERT, DOC]:
        if not path.exists():
            raise SystemExit(f"missing file: {path}")

    subprocess.run(["lake", "env", "lean", str(LEAN)], cwd=ROOT, check=True)

    data = json.loads(CERT.read_text(encoding="utf-8"))
    text = DOC.read_text(encoding="utf-8")
    lean = LEAN.read_text(encoding="utf-8")
    combined = text + "\n" + lean + "\n" + json.dumps(data, sort_keys=True)

    if data.get("status") != "CPOL_TYPE_GATE_CLOSED_ONLY":
        raise SystemExit("status mismatch")
    if data.get("theorem_closure") is not False:
        raise SystemExit("theorem_closure must remain false")
    if data.get("type_family") != "TChr : Nat -> Type":
        raise SystemExit("type_family mismatch")
    if data.get("definition") != "inductive TChr (n : Nat) : Type | base : TChr n":
        raise SystemExit("definition mismatch")

    for token in TOKENS:
        if token not in text:
            raise SystemExit(f"missing token in doc: {token}")
        if token not in data.get("machine_tokens", []):
            raise SystemExit(f"missing token in json: {token}")

    for required in [
        "inductive TChr",
        "inductive TChr",
        "tChrCanonicalWitness",
        "tChr_nonempty",
        "tChr_decidableEq_exists",
    ]:
        if required not in lean:
            raise SystemExit(f"missing Lean declaration: {required}")

    for forbidden in FORBIDDEN:
        if forbidden in combined:
            raise SystemExit(f"forbidden overclaim detected: {forbidden}")

    print("Chronos CPOL type gate verified: CPOL_TYPE_GATE_CLOSED_ONLY")

if __name__ == "__main__":
    main()
