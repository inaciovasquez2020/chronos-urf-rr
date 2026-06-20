#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(".")
LEAN_ROOT = ROOT / "lean"

DEF_CANDIDATE = re.compile(r"\b(def|abbrev|structure|inductive|class)\s+CandidateChord\b")
DEF_MARKED = re.compile(r"\b(def|abbrev|structure|inductive|class)\s+MarkedBoundaryChord\b")

EXPLICIT_IDENTITY = [
    re.compile(r"\bDOMAIN_IDENTITY\s*\(\s*MarkedBoundaryChord\s*,\s*CandidateChord\s*\)"),
    re.compile(r"\bDOMAIN_IDENTITY\s*\(\s*CandidateChord\s*,\s*MarkedBoundaryChord\s*\)"),
    re.compile(r"\bMarkedBoundaryChord\s*=\s*CandidateChord\b"),
    re.compile(r"\bCandidateChord\s*=\s*MarkedBoundaryChord\b"),
    re.compile(r"\bmarkedBoundaryChord_candidateChord_domain_identity\b"),
    re.compile(r"\bcandidateChord_markedBoundaryChord_domain_identity\b"),
]


def lean_files():
    if not LEAN_ROOT.exists():
        return []
    return sorted(p for p in LEAN_ROOT.rglob("*.lean") if p.is_file())


def collect(pattern: re.Pattern[str]):
    out = []
    for path in lean_files():
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                out.append((path, line_no, line.strip()))
    return out


def collect_any(patterns):
    out = []
    for path in lean_files():
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(p.search(line) for p in patterns):
                out.append((path, line_no, line.strip()))
    return out


def fail(label: str, matches=None) -> None:
    print(f"R1_DOMAIN_IDENTITY_FAIL := {label}")
    if matches:
        print("OBSERVED_MATCHES :=")
        for path, line_no, line in matches[:20]:
            print(f"  {path}:{line_no}: {line}")
    raise SystemExit(1)


def main() -> None:
    candidate_defs = collect(DEF_CANDIDATE)
    marked_defs = collect(DEF_MARKED)
    identity = collect_any(EXPLICIT_IDENTITY)

    if not candidate_defs:
        fail("MISSING_LEAN_DEFINITION(CandidateChord)")
    if not marked_defs:
        fail("MISSING_LEAN_DEFINITION(MarkedBoundaryChord)")
    if not identity:
        fail("MISSING_EXPLICIT_LEAN_DOMAIN_IDENTITY(MarkedBoundaryChord, CandidateChord)")

    print("R1_DOMAIN_IDENTITY_OK")


if __name__ == "__main__":
    main()
