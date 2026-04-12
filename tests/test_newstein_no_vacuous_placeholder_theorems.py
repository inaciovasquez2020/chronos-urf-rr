from pathlib import Path
import re

FILES = [
    "lean/Newstein/ParentDepthDecrement.lean",
    "lean/Newstein/RootedBallTrivialization.lean",
    "lean/Newstein/FiberQuotientRank.lean",
    "lean/Newstein/DirectSumIndependence.lean",
    "lean/Newstein/PerStepInformationBound.lean",
    "lean/Newstein/QuotientGapClosure.lean",
]

FORBIDDEN_PATTERNS = [
    r":\s*Prop\s*:=\s*by\s*trivial",
    r"^axiom\s+",
]

REQUIRED_NAMES = [
    "ParentDepthDecrement",
    "RootedBallTrivialization",
    "FiberQuotientRank",
    "DirectSumIndependence",
    "PerStepInformationBound",
    "QuotientGapClosure",
]

def test_named_theorems_exist():
    missing = []
    for fp, name in zip(FILES, REQUIRED_NAMES):
        s = Path(fp).read_text()
        if f"theorem {name}" not in s:
            missing.append((fp, name))
    assert not missing, f"missing theorem declarations: {missing}"

def test_placeholder_inventory_is_explicit():
    bad = []
    for fp in FILES:
        s = Path(fp).read_text()
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, s, flags=re.M):
                bad.append((fp, pat))
    assert bad, "expected current placeholder inventory to remain explicit"

def test_closure_is_marked_conditional_while_placeholders_exist():
    s = Path("docs/math/NEWSTEIN_QUOTIENT_GAP_CLOSURE_TARGET.md").read_text()
    placeholders = []
    for fp in FILES:
        t = Path(fp).read_text()
        if re.search(r":\s*Prop\s*:=\s*by\s*trivial", t) or re.search(r"^axiom\s+", t, flags=re.M):
            placeholders.append(fp)
    if placeholders:
        assert "Status: CONDITIONAL" in s
        assert "QuotientGapClosure^conditional" in s
