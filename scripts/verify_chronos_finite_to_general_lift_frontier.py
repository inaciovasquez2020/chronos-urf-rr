from pathlib import Path

DOC = Path("docs/status/CHRONOS_FINITE_TO_GENERAL_LIFT_FRONTIER_2026_05_02.md")

REQUIRED = [
    "Status: THEOREM FRONTIER / NEXT MISSING LEMMA",
    "Prior Closed Surface",
    "Next Missing Lemma",
    "finite-to-general lift",
    "\\operatorname{COR}_R(G_i)\\ge \\alpha |V(G_i)|",
    "\\operatorname{COR}_R(G_n)\\ge \\alpha' |V(G_n)|",
    "Required Additional Structure",
    "a graph-family constructor \\(G_n\\)",
    "a certificate generator \\(C(n)\\)",
    "This document isolates the next missing theorem-level bridge only.",
    "It does not prove the finite-to-general lift.",
    "It does not prove the locality-to-depth bridge.",
    "It does not prove theorem-level Chronos closure.",
    "It does not assert that finite evidence alone implies an infinite-family theorem.",
    "It does not assert that the finite-to-general lift is the only remaining global Chronos theorem obligation.",
    "Next Admissible Object",
]

FORBIDDEN = [
    "Chronos is solved",
    "finite-to-general lift is proved",
    "locality-to-depth bridge is proved",
    "theorem-level Chronos closure is proved",
    "STATUS: finite evidence alone implies an infinite-family theorem",
    "P vs NP is solved",
]

def main() -> None:
    text = DOC.read_text()
    missing = [token for token in REQUIRED if token not in text]
    forbidden = [token for token in FORBIDDEN if token in text]
    if missing:
        raise SystemExit(f"missing required tokens: {missing}")
    if forbidden:
        raise SystemExit(f"forbidden overclaim tokens: {forbidden}")
    print("Chronos finite-to-general lift frontier verification OK.")

if __name__ == "__main__":
    main()
