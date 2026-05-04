import json
from pathlib import Path

doc = Path("docs/status/CHRONOS_CERTIFICATE_EMBEDDING_INTERFACE_2026_05_04.md")
cert = Path("artifacts/chronos/chronos_certificate_embedding_interface_2026_05_04.json")

text = doc.read_text(encoding="utf-8")
data = json.loads(cert.read_text(encoding="utf-8"))

required_doc_tokens = [
    "CERTIFIED_INTERFACE_ONLY",
    "THEOREM_CLOSURE_FALSE",
    "CHRONOS_CLOSURE_FALSE",
    "H4_1_FGL_CLOSURE_FALSE",
    "P_VS_NP_CLAIM_FALSE",
    "CHRONOS_CERTIFICATE_EMBEDDING_NAMED",
    "E_N_INTERFACE_DEFINED",
    "CERTIFICATE_INSTANCE_SPACE_C_N_REQUIRED",
    "CERTIFICATE_DISTRIBUTION_NU_N_REQUIRED",
    "PUSHFORWARD_UNIFORMITY_REQUIRED",
    "ADMISSIBILITY_PRESERVATION_REQUIRED",
    "CERTIFICATE_CONSTANT_BINDING_REQUIRED",
    "NO_E_N_CONSTRUCTION_CLAIM",
    "E_n:C_n\\to \\{0,1\\}^n",
    "(E_n)_*\\nu_n=\\mu_n",
    "c_{\\mathrm{repo}}>0",
]

for token in required_doc_tokens:
    if token not in text:
        raise SystemExit(f"missing doc token: {token}")

expected = {
    ("status",): "CERTIFIED_INTERFACE_ONLY",
    ("theorem_closure",): False,
    ("chronos_closure",): False,
    ("h4_1_fgl_closure",): False,
    ("named_missing_object",): "ChronosCertificateEmbedding",
    ("interface", "embedding_symbol"): "E_n",
    ("interface", "domain"): "repository_certificate_instances_C_n",
    ("interface", "codomain"): "{0,1}^n",
}

for path, value in expected.items():
    node = data
    for key in path:
        node = node[key]
    if node != value:
        raise SystemExit(f"bad value at {'.'.join(path)}: {node!r}")

required_obligations = [
    "Define repository certificate instance space C_n explicitly.",
    "Define certificate distribution nu_n explicitly.",
    "Construct E_n explicitly.",
    "Prove pushforward uniformity or replace uniformity with a certified nonuniform IC lower bound.",
    "Prove Search_F_n compatibility.",
    "Prove Chronos admissibility preservation.",
    "Derive c_repo > 0 from repository certificate constants."
]

for obligation in required_obligations:
    if obligation not in data["obligations"]:
        raise SystemExit(f"missing obligation: {obligation}")

for forbidden in [
    "Chronos is solved",
    "H4.1 is proved",
    "FGL is proved",
    "P vs NP is solved",
    "theorem_closure\": true",
    "chronos_closure\": true",
    "h4_1_fgl_closure\": true",
    "constructs E_n",
    "proves pushforward uniformity",
]:
    hay = text.lower() + "\n" + json.dumps(data).lower()
    if forbidden.lower() in hay:
        raise SystemExit(f"forbidden overclaim detected: {forbidden}")

print("ChronosCertificateEmbedding interface verified: CERTIFIED_INTERFACE_ONLY")
