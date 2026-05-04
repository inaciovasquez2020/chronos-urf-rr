import json
from pathlib import Path

doc = Path("docs/status/EXPLICIT_IC_BRIDGE_CONTRACT_2026_05_04.md")
cert = Path("artifacts/chronos/explicit_ic_bridge_contract_2026_05_04.json")

doc_text = doc.read_text(encoding="utf-8")
data = json.loads(cert.read_text(encoding="utf-8"))

required_doc_tokens = [
    "CONDITIONAL_BRIDGE_CONTRACT",
    "THEOREM_CLOSURE_FALSE",
    "CHRONOS_CLOSURE_FALSE",
    "H4_1_FGL_CLOSURE_FALSE",
    "P_VS_NP_CLAIM_FALSE",
    "F_N_EXPLICIT",
    "MU_N_EXPLICIT",
    "SEARCH_F_N_EXPLICIT",
    "IC_LOWER_BOUND_EXPLICIT",
    "CONSTANT_C_EQUALS_1",
    "CERTIFICATE_CONSTANT_BINDING_FALSE",
    "MISSING_OBJECT_CHRONOS_CERTIFICATE_EMBEDDING",
    "F_n := \\{0,1\\}^n",
    "\\mu_n := \\operatorname{Unif}(\\{0,1\\}^n)",
    "\\operatorname{Search}_{F_n}(x) := x",
    "IC_{\\mu_n}(\\operatorname{Search}_{F_n}) \\ge c n",
    "c := 1",
]

for token in required_doc_tokens:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

expected = {
    ("status",): "CONDITIONAL_BRIDGE_CONTRACT",
    ("theorem_closure",): False,
    ("chronos_closure",): False,
    ("h4_1_fgl_closure",): False,
    ("objects", "F_n"): "{0,1}^n",
    ("objects", "mu_n"): "uniform_distribution_on_{0,1}^n",
    ("objects", "Search_F_n"): "identity_search_functional_Search_F_n(x)=x",
    ("ic_lower_bound", "entropy_H_mu_n_X"): "n",
    ("ic_lower_bound", "information_cost_IC_mu_n_Search_F_n"): "n",
    ("ic_lower_bound", "constant_c"): 1,
    ("repository_binding", "bound_to_certificate_constants"): False,
    ("repository_binding", "missing_binding_object"): "ChronosCertificateEmbedding",
}

for path, value in expected.items():
    node = data
    for key in path:
        node = node[key]
    if node != value:
        raise SystemExit(f"bad certificate value at {'.'.join(path)}: {node!r}")

for forbidden in [
    "P vs NP is solved",
    "Chronos is solved",
    "H4.1 is proved",
    "FGL is proved",
    "theorem-level closure true",
    "bound_to_certificate_constants\": true",
]:
    if forbidden.lower() in doc_text.lower() or forbidden.lower() in json.dumps(data).lower():
        raise SystemExit(f"forbidden overclaim detected: {forbidden}")

print("Explicit IC bridge contract verified: CONDITIONAL_BRIDGE_CONTRACT")
