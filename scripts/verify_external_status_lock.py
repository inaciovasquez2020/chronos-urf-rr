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
    ("Verify operator norm perturbation boundary", "python3 tools/verifier/verify_operator_norm_perturbation_boundary.py"),
    ("Verify known gravity limit boundary", "python3 tools/verifier/verify_gravity_boundary.py"),
    ("Verify gravity program closeout boundary", "python3 tools/verifier/verify_gravity_program_closeout_boundary.py"),
    ("Verify metric stress energy action triple boundary", "python3 tools/verifier/verify_metric_stress_energy_action_triple_boundary.py"),
    ("Verify Einstein Hilbert target law boundary", "python3 tools/verifier/verify_einstein_hilbert_target_law_boundary.py"),
    ("Verify pregeometric bridge continuum limit boundary", "python3 tools/verifier/verify_pregeometric_bridge_continuum_limit_boundary.py"),
    ("Verify Chronos spectral operator root boundary", "python3 tools/verifier/verify_chronos_spectral_operator_root_boundary.py"),
    ("Verify Chronos root spectral solve boundary", "python3 tools/verifier/verify_chronos_root_spectral_solve_boundary.py"),
    ("Verify Chronos root gauge invariant trace boundary", "python3 tools/verifier/verify_chronos_root_gauge_invariant_trace_boundary.py"),
    ("Verify Chronos root finite spectral layer closeout boundary", "python3 tools/verifier/verify_chronos_root_finite_spectral_layer_closeout_boundary.py"),
    ("Verify gravity metric backreaction boundary", "python3 tools/verify_gravity_metric_backreaction_boundary_2026_06_27.py"),
    ("Verify external status lock", "python3 scripts/verify_external_status_lock.py"),
    ("Verify certificate constant binding boundary", "python3 tools/verifier/verify_certificate_constant_binding_boundary.py"),
    ("Verify restricted package theorem surface boundary", "python3 tools/verifier/verify_restricted_package_theorem_surface_boundary.py"),
    ("Verify literature nonclaim audit", "python3 tools/verify_literature_nonclaim_audit.py"),
    ("Verify known closed Cantor boundary demo", "python3 tools/verifier/verify_known_closed_cantor_boundary_demo.py"),
    ("Verify Chronos semantic derivation rules boundary", "python3 tools/verifier/verify_chronos_semantic_derivation_rules_boundary.py"),
]

workflow_steps = []
current_name = None

for line in workflow_lines:
    s = line.strip()
    if s.startswith("- name: "):
        current_name = s.removeprefix("- name: ").strip()
        continue
    if s.startswith("run: ") and current_name is not None:
        run_cmd = s.removeprefix("run: ").strip()
        workflow_steps.append((current_name, run_cmd))
        current_name = None

for name, cmd in required_workflow_steps:
    if (name, cmd) not in workflow_steps:
        raise SystemExit(
            "missing required status-lock workflow step pair: "
            f"name={name!r}, run={cmd!r}"
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
