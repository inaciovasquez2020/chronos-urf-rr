from pathlib import Path

DOC = Path("docs/status/CHRONOS_CERTIFIED_OBSTRUCTION_RANK_DEFINITION_2026_05_02.md")

REQUIRED = [
    "Status: DEFINITION LOCK / THEOREM FRONTIER INPUT",
    "Certified Obstruction Rank",
    "\\operatorname{COR}_R(G)",
    "\\dim_{\\mathbb F_2}\\bigl(Z_1(G)/L_R(G)\\bigr)",
    "Family-Level Growth Input",
    "\\operatorname{COR}_R(G_n)\\ge \\alpha |V(G_n)|",
    "This document fixes a definition only.",
    "It does not prove the Chronos theorem-level closure.",
    "It does not prove the finite-to-general lift.",
    "It does not prove the locality-to-depth bridge.",
    "Weakest Missing Lemma",
]

FORBIDDEN = [
    "Chronos is solved",
    "theorem-level closure is proved",
    "unconditional Chronos closure",
    "P vs NP is solved",
    "Clay problem is solved",
]

def main() -> None:
    text = DOC.read_text()
    missing = [token for token in REQUIRED if token not in text]
    forbidden = [token for token in FORBIDDEN if token in text]
    if missing:
        raise SystemExit(f"missing required tokens: {missing}")
    if forbidden:
        raise SystemExit(f"forbidden overclaim tokens: {forbidden}")
    print("Chronos certified obstruction rank definition verification OK.")

if __name__ == "__main__":
    main()
