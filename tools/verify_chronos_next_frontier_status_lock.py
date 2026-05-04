from pathlib import Path

p = Path("docs/status/CHRONOS_NEXT_FRONTIER_STATUS_LOCK_2026_05_04.md")
text = p.read_text(encoding="utf-8")

required = [
    "CERTIFIED_FRONTIER_ONLY",
    "THEOREM_CLOSURE_FALSE",
    "NO_P_VS_NP_CLAIM",
    "NO_UNCONDITIONAL_ENTROPYDEPTH_CLAIM",
    "NO_H4_1_FGL_CLOSURE_CLAIM",
    "MISSING_OBJECT_EXPLICIT_IC_LOWER_BOUND",
    "IC_{\\mu_n}(\\operatorname{Search}_{F_n}) \\ge c n",
]

for token in required:
    if token not in text:
        raise SystemExit(f"missing required token: {token}")

forbidden = [
    "P vs NP is solved",
    "P≠NP is proved",
    "EntropyDepth is unconditionally closed",
    "H4.1 is proved",
    "FGL is proved",
    "theorem-level closure",
]

lower = text.lower()
for phrase in forbidden:
    if phrase.lower() in lower and "does not claim theorem-level closure" not in lower:
        raise SystemExit(f"forbidden overclaim detected: {phrase}")

print("Chronos next frontier status lock verified: CERTIFIED_FRONTIER_ONLY")
