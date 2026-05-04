#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "artifacts/chronos/certificates/chronos_certificate_embedding_frontier_2026_05_04.json"
DOC = ROOT / "docs/status/CHRONOS_CERTIFICATE_EMBEDDING_FRONTIER_2026_05_04.md"

REQUIRED_JSON = {
    "artifact": "ChronosCertificateEmbeddingFrontier",
    "status": "FRONTIER_OPEN",
    "theorem_closure": False,
    "missing_object": "ChronosCertificateEmbedding",
}

REQUIRED_TOKENS = [
    "CHRONOS_CERTIFICATE_EMBEDDING_FRONTIER",
    "FRONTIER_OPEN",
    "THEOREM_CLOSURE_FALSE",
    "H4_1_FGL_CLOSURE_FALSE",
    "IC_CONTRACT_EXPLICIT",
    "CERTIFICATE_EMBEDDING_MISSING",
    "REPO_CONSTANT_BINDING_MISSING",
]

FORBIDDEN_CLAIMS = [
    "THEOREM_CLOSURE_TRUE",
    "H4_1_FGL_CLOSURE_TRUE",
    "P_VS_NP_PROVED",
    "CHRONOS_SOLVED",
    "CERTIFICATE_EMBEDDING_PROVED",
    "REPO_CONSTANT_BINDING_TRUE",
]

def main() -> None:
    assert CERT.exists(), f"missing certificate: {CERT}"
    assert DOC.exists(), f"missing status doc: {DOC}"

    data = json.loads(CERT.read_text())
    text = DOC.read_text()

    for key, value in REQUIRED_JSON.items():
        assert data.get(key) == value, f"{key} mismatch: {data.get(key)!r} != {value!r}"

    assert data["explicit_ic_contract"]["F_n"] == "{0,1}^n"
    assert data["explicit_ic_contract"]["mu_n"] == "Uniform({0,1}^n)"
    assert data["explicit_ic_contract"]["Search_F_n"] == "identity"
    assert data["explicit_ic_contract"]["IC_lower_bound"] == "n"
    assert data["explicit_ic_contract"]["c"] == 1

    req = data["required_completion"]
    assert req["certificate_space"] == "C_n"
    assert req["certificate_distribution"] == "nu_n"
    assert req["embedding"] == "E_n : C_n -> {0,1}^n"
    assert req["locality_preservation"] is True
    assert req["admissibility_preservation"] is True
    assert req["finite_patch_preservation"] is True
    assert req["repo_constant_binding"] == "c_repo > 0"

    for token in REQUIRED_TOKENS:
        assert token in text, f"missing token in doc: {token}"
        assert token in data["machine_tokens"], f"missing token in json: {token}"

    combined = text + "\n" + json.dumps(data)
    for claim in FORBIDDEN_CLAIMS:
        assert claim not in combined, f"forbidden overclaim: {claim}"

    print("Chronos certificate embedding frontier verified: FRONTIER_OPEN")

if __name__ == "__main__":
    main()
