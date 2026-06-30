#!/usr/bin/env python3
from pathlib import Path
import re
import sys

status = Path("docs/status/EXTERNAL_STATUS_LOCK.md")
if not status.exists():
    raise SystemExit("missing docs/status/EXTERNAL_STATUS_LOCK.md")

text = status.read_text(encoding="utf-8")

required = [
    "Axioms, admits, `sorry`, placeholder witnesses, string witnesses, dashboards, ledgers, and narrative wrappers are not theorem proofs.",
    "CI/build success means the checked surface compiles or verifies; it does not upgrade conditional mathematics into theorem-level closure.",
    "Any result depending on an axiom, admit, `sorry`, synthetic placeholder, or explicitly named missing lemma is conditional.",
    "Forbidden public description:",
]

for s in required:
    if s not in text:
        raise SystemExit(f"missing required status boundary: {s}")

workflow = Path(".github/workflows/external-status-lock.yml")
if not workflow.exists():
    raise SystemExit("missing .github/workflows/external-status-lock.yml")

workflow_lines = workflow.read_text(encoding="utf-8").splitlines()

required_workflow_steps = [
    (
        "Verify operator norm perturbation boundary",
        "python3 tools/verify_operator_norm_perturbation_boundary.py",
    ),
    (
        "Verify known gravity limit boundary",
        "python3 tools/verifier/verify_gravity_boundary.py",
    ),
    (
        "Verify gravity metric backreaction boundary",
        "python3 tools/verify_gravity_metric_backreaction_boundary_2026_06_27.py",
    ),
    (
        "Verify external status lock",
        "python3 scripts/verify_external_status_lock.py",
    ),
    (
        "Verify literature nonclaim audit",
        "python3 tools/verify_literature_nonclaim_audit.py",
    ),
]

workflow_steps = []
current_name = None

for line in workflow_lines:
    stripped = line.strip()
    if stripped.startswith("- name: "):
        current_name = stripped.removeprefix("- name: ").strip()
        continue
    if current_name is not None and stripped.startswith("run: "):
        workflow_steps.append((current_name, stripped.removeprefix("run: ").strip()))
        current_name = None

for step in required_workflow_steps:
    if step not in workflow_steps:
        name, command = step
        raise SystemExit(
            "missing required status-lock workflow step pair: "
            f"name={name!r}, run={command!r}"
        )

readme_paths = [Path("README.md"), Path("README"), Path("readme.md")]
readme_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in readme_paths if p.exists())

dangerous_patterns = [
    r"\bwe prove the Riemann Hypothesis\b",
    r"\bwe prove RH\b",
    r"\bwe prove P\s*(?:!=|≠)\s*NP\b",
    r"\bwe prove the Hodge Conjecture\b",
    r"\bwe prove (?:BSD|Birch[-– ]Swinnerton[-– ]Dyer)\b",
    r"\bwe prove Navier[-– ]Stokes\b",
    r"\bwe prove Yang[-– ]Mills\b",
    r"\bwe prove the mass gap\b",
    r"\bwe solve the Clay\b",
    r"\bMillennium Prize solution\b",
    r"\bunconditional solution\b",
    r"\btheorem-complete solution\b",
]

for pat in dangerous_patterns:
    if re.search(pat, readme_text, flags=re.IGNORECASE):
        raise SystemExit(f"dangerous README claim matched: {pat}")

print("external status lock: PASS")
