#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/status/CHRONOS_PREFIX_CONDITIONING_EMBEDDING_2026_05_03.md"
ART = ROOT / "artifacts/chronos/prefix_conditioning_embedding_2026_05_03.json"

REQUIRED_DOC = [
    "Status: CONDITIONAL_PREFIX_EMBEDDING_REDUCTION",
    "Sample public randomness",
    "\\sigma\\sim \\mathrm{Unif}(S_n)",
    "\\alpha_i^\\sigma",
    "I(X_{\\sigma(i)};T\\mid Y,X_{\\sigma(<i)})",
    "\\beta_i^\\sigma",
    "I(Y_{\\sigma(i)};T\\mid X,Y_{\\sigma(<i)})",
    "IC_{\\mu_n}(\\Pi)",
    "\\sum_{i=1}^n",
    "\\mathbb E_\\sigma[",
    "\\mathbb E_{\\sigma,I}",
    "\\frac1n IC_{\\mu_n}(\\Pi)",
    "\\mathrm{PrefixEmb}_n",
    "IC_\\zeta(\\mathrm{PrefixEmb}_n(\\Pi))",
    "n^{-1}IC_{\\mu_n}(\\Pi)",
    "C_{k,5,k+1}=2^{8k}k^{2k}5^{3k}",
    "T_n=\\Omega_k(n)",
    "Minimal Remaining Object",
    "\\mathrm{PrefixEmb}_{n\\#}\\zeta=\\mu_n"
]

FORBIDDEN_DOC = [
    "P≠NP is proved",
    "P != NP is proved",
    "unconditional theorem-level closure is proved",
    "terminal Chronos lower bound is proved",
    "frontier closed unconditionally",
    "solves P vs NP"
]

REQUIRED_JSON = {
    "artifact_class": "CHRONOS_PREFIX_CONDITIONING_EMBEDDING",
    "status": "CONDITIONAL_PREFIX_EMBEDDING_REDUCTION",
    "replaces_false_lemma": "leave_one_out_coordinate_reveal_bound",
    "replacement": "prefix_conditioning_chain_rule_bound",
    "conditional_embedding_bound": "IC_zeta(PrefixEmb_n(Pi)) <= (1/n)IC_mu(Pi)",
    "minimal_remaining_object": "PrefixEmb_{n#} zeta = mu_n on the exact repository search distribution"
}

def fail(msg: str) -> None:
    print(f"Chronos prefix-conditioning embedding verification failed: {msg}", file=sys.stderr)
    sys.exit(1)

def main() -> None:
    if not DOC.exists():
        fail(f"missing doc {DOC}")
    if not ART.exists():
        fail(f"missing artifact {ART}")

    text = DOC.read_text()

    for needle in REQUIRED_DOC:
        if needle not in text:
            fail(f"missing required doc token: {needle}")

    for bad in FORBIDDEN_DOC:
        if bad in text:
            fail(f"forbidden overclaim token present: {bad}")

    data = json.loads(ART.read_text())

    for key, value in REQUIRED_JSON.items():
        if data.get(key) != value:
            fail(f"bad artifact field {key}: expected {value!r}, got {data.get(key)!r}")

    boundary = data.get("boundary", {})
    if boundary.get("unconditional_theorem_closure") is not False:
        fail("boundary must keep unconditional_theorem_closure=false")
    if boundary.get("p_not_np_claim") is not False:
        fail("boundary must keep p_not_np_claim=false")
    if boundary.get("terminal_chronos_lower_bound_claimed") is not False:
        fail("boundary must keep terminal_chronos_lower_bound_claimed=false")
    if boundary.get("frontier_preserved") is not True:
        fail("boundary must keep frontier_preserved=true")

    print("Chronos prefix-conditioning embedding verified: CONDITIONAL_PREFIX_EMBEDDING_REDUCTION")

if __name__ == "__main__":
    main()
