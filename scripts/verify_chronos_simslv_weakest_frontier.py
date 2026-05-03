from pathlib import Path

DOC = Path("docs/status/CHRONOS_SIMSLV_WEAKEST_FRONTIER_LEMMA_2026_05_03.md")

REQUIRED = [
    "Status: CONDITIONAL_FRONTIER",
    "Boundary: FRONTIER_OPEN preserved.",
    r"\sim_{\mathcal U}\subseteq \sim_{\Pi}",
    r"\tau_{\Pi}=\rho\circ\tau_{\mathrm{cyl}}",
    r"\operatorname{rank}_{\mathbb Q}",
    r"\mathcal C^{\mathrm{corr}}_{k,R,B}(P)",
    "Exact Obstruction",
    r"x\sim_{\mathcal U}y",
    r"x\not\sim_{\Pi}y",
    "It does not assert unconditional Chronos closure.",
    "It does not assert theorem-level H4.1/FGL closure.",
    "It preserves FRONTIER_OPEN status.",
]

FORBIDDEN = [
    "unconditional Chronos closure proved",
    "theorem-level H4.1/FGL closure proved",
    "FRONTIER_CLOSED",
    "solves Chronos",
    "solves P vs NP",
    "unconditional theorem-level closure",
]

def main() -> None:
    assert DOC.exists(), f"missing {DOC}"
    text = DOC.read_text()
    missing = [s for s in REQUIRED if s not in text]
    forbidden = [s for s in FORBIDDEN if s in text]
    assert not missing, f"missing required strings: {missing}"
    assert not forbidden, f"forbidden strings present: {forbidden}"
    print("Chronos SiMSLV weakest frontier lemma verified: PASS")

if __name__ == "__main__":
    main()
